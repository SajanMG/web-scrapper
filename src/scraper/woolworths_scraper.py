from scrapling.fetchers import DynamicFetcher
from playwright.sync_api import Page

from extractors import extract_woolworths_product
from woolworths_extractor import extract_woolworths_raw_products


def search_woolworths(search_term: str):
    products = []
    next_url = None

    def extract_products(page: Page):
        nonlocal next_url
        page.wait_for_function("""
            () => {
                const tiles = document.querySelectorAll("wc-product-tile");

                if (tiles.length === 0) {
                    return false;
                }

                return Array.from(tiles).some(tile => {
                    if (!tile.shadowRoot) {
                        return false;
                    }

                    const title = tile.shadowRoot.querySelector(
                        ".product-title-container .title a"
                    );

                    const price = tile.shadowRoot.querySelector(
                        ".product-tile-price .primary"
                    );

                    return title !== null && price !== null;
                });
            }
        """, timeout=30000)
              
        
        raw_products = extract_woolworths_raw_products(page)


        for raw_product in raw_products:
            product = extract_woolworths_product(raw_product)
            products.append(product)

            
        next_url = page.locator('a[rel="next"]').get_attribute("href")


    search_url = (
        "https://www.woolworths.com.au/shop/search/products"
        f"?searchTerm={search_term}"
    )

    current_url = search_url

    while current_url:
        next_url = None
        print("Fetching:", current_url)

        DynamicFetcher.fetch(
            current_url,
            page_action=extract_products
        )
        print("Next:", next_url)

        if next_url:
            current_url = (
                "https://www.woolworths.com.au" + next_url
            )
        else:
            current_url = None

    return products

results = search_woolworths("eggs")

print("Products:", len(results))

for product in results:
    print(product.to_dict())