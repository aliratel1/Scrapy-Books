import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            book_page = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in book_page:
                book_url = 'https://books.toscrape.com/' + book_page
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + book_page
            yield response.follow(book_url, callback = self.book_details)
        
        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)
        
    def book_details(self, response):
        tables = response.css("table tr")
        yield {
            'url' : response.url,
            'title' : response.css('.product_main h1 ::text').get(),
            'price' : response.css('.price_color ::text').get(),
            'description' : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'book Type' : response.xpath("//ul[@class='breadcrumb']/li/following-sibling::li[2]/a/text()").get(),
            'Number of reviews' : tables[6].css('td ::text').get(),
        }