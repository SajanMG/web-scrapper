from scrapling.fetchers import DynamicFetcher
from playwright.sync_api import Page

from extractors import extract_woolworths_product
from woolworths_extractor import extract_woolworths_raw_products


def search_woolworths(search_term: str):
    products = []

    def extract_products(page: Page):
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

            

    search_url = (
        "https://www.woolworths.com.au/shop/search/products"
        f"?searchTerm={search_term}"
    )

    DynamicFetcher.fetch(
        search_url,
        page_action=extract_products
    )

    return products

results = search_woolworths("eggs")

print("Products:", len(results))

for product in results:
    print(product.to_dict())