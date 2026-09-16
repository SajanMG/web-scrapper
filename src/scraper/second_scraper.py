import logging

from scrapling.spiders import Spider, Response
from extractors import extract_scrapingcourse_product

class SecondScraper(Spider):
    name = "dress"
    logging_level = logging.WARNING

    start_urls = [
        "https://www.scrapingcourse.com/pagination"
    ]

    async def parse(self, response:Response):
        print("Processing:", response.url)
        products = response.css(".product-item")    

        for product in products:
            product_data = extract_scrapingcourse_product(product)
            yield product_data.to_dict()

        next_page = response.css(".next-page::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse
            )

result = SecondScraper().start()

print("Items scraped:", len(result.items))
print("First item:", result.items[0])