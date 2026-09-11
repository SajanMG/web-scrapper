from scrapling.fetchers import Fetcher
from urllib.parse import urljoin

page = Fetcher.get("https://books.toscrape.com/")

books = page.css("article.product_pod")

print("Book cards:", len(books))

for book in books:
    title = book.css("h3 a::attr(title)").get()
    price_text = book.css(".price_color::text").get()
    price = float(price_text.replace("£", ""))

    availability_text = book.css(".availability::text").getall()

    availability_text = " ".join(
        text.strip()
        for text in availability_text
        if text.strip()
    )
    
    product_path = book.css("h3 a::attr(href)").get()
    product_url = urljoin("https://books.toscrape.com/", product_path)
    available = availability_text.lower() == "in stock"


    print({
    "name": title,
    "price": price,
    "currency": "GBP",
    "available": available,
    "product_url": product_url,
    "source": "books.toscrape.com"
})

# OUTSIDE the loop
first_book_path = books[0].css("h3 a::attr(href)").get()

first_book_url = urljoin(
    "https://books.toscrape.com/",
    first_book_path
)

product_page = Fetcher.get(first_book_url)

print("Product page:", first_book_url)
print("H1:", product_page.css("h1::text").get())