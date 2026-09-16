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
        price=price,
        currency="GBP",
        product_url=response.url,
        source="books.toscrape.com"
    )