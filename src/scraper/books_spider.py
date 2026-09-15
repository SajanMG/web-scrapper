from scrapling.spiders import Spider, Response
from models import Product

class BooksSpider(Spider):
    name = "books"

    start_urls = [
        "https://books.toscrape.com/"
    ]

    async def parse(self, response: Response):
        books = response.css("article.product_pod")

        print("Books found:", len(books))

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
        title = response.css("h1::text").get()

        price_text = response.css(
            ".price_color::text"
        ).get()

        # description = response.css(
        #     "#product_description + p::text"
        # ).get()

        price = float(
            price_text.replace("£", "")
        )

        # print("Title:", title)
        # print("Price:", price)
        # print("Description:", description)

        product = Product(
            name=title,
            price=price,
            currency="GBP",
            product_url=response.url,
            source="books.toscrape.com"
        )

        yield product.to_dict()


result = BooksSpider().start()

print(result.items)