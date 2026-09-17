from models import Product


def extract_book(response) -> Product:
    title = response.css("h1::text").get()

    price_text = response.css(
        ".price_color::text"
    ).get()

    price = float(
        price_text.replace("£", "")
    )

    return Product(
        name=title,
        current_price=price,
        currency="GBP",
        product_url=response.url,
        source="books.toscrape.com"
    )


def extract_scrapingcourse_product(product) -> Product:
    name = product.css(".product-name::text").get()
    price_text = product.css(".product-price::text").get()

    price = float(
        price_text.replace("$", "")
    )
    product_url = product.css("a::attr(href)").get()

    return Product(
        name=name,
        current_price=price,
        currency="USD",
        product_url=product_url,
        source="scrapingcourse.com"
    )