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

def extract_woolworths_product(raw_product) -> Product:
    current_price = float(
        raw_product["current_price"].replace("$", "")
    )

    regular_price = None

    if raw_product["regular_price"]:
        regular_price = float(
            raw_product["regular_price"].replace("$", "")
        )

    unit_price = None
    unit = None

    if raw_product["unit_price"]:
        parts = raw_product["unit_price"].split("/")

        unit_price = float(
            parts[0].replace("$", "").strip()
        )

        unit = parts[1].strip()

    return Product(
        name=raw_product["name"],
        current_price=current_price,
        currency="AUD",
        product_url=raw_product["product_url"],
        source="woolworths.com.au",
        regular_price=regular_price,
        unit_price=unit_price,
        unit=unit,
        on_special=regular_price is not None
    )