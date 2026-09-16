import logging

from scrapling.spiders import Spider, Response
from extractors import extract_book

class BooksSpider(Spider):
    name = "books"

    logging_level = logging.WARNING

    start_urls = [
        "https://books.toscrape.com/"
    ]

    async def parse(self, response: Response):
        print("Processing:", response.url)
        books = response.css("article.product_pod")


        for book in books:
            product_path = book.css(
                "h3 a::attr(href)"
            ).get()

            yield response.follow(
                product_path,
                callback=self.parse_product
            )

        next_page = response.css(
            "li.next a::attr(href)"
        ).get()
        
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse
            )

    async def parse_product(self, response: Response):
        product = extract_book(response)

        yield product.to_dict()


result = BooksSpider().start()

print("Items scraped:", len(result.items))
print("First item:", result.items[0])