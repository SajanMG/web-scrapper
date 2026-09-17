from scrapling.fetchers import DynamicFetcher
from playwright.sync_api import Page

from extractors import extract_woolworths_product


def search_woolworths(search_term: str):
    products = []

    def extract_products(page: Page):
        page.locator("wc-product-tile").first.wait_for(
            state="attached",
            timeout=30000
        )

        raw_products = page.evaluate("""
            () => {
                const tiles =
                    document.querySelectorAll("wc-product-tile");

                const results = Array.from(tiles).map(tile => {
                    if (!tile.shadowRoot) {
                        return null;
                    }

                    const root = tile.shadowRoot;

                    return {
                        name: root.querySelector(
                            ".product-title-container .title a"
                        )?.textContent.trim() || null,

                        current_price: root.querySelector(
                            ".product-tile-price .primary"
                        )?.textContent.trim() || null,

                        unit_price: root.querySelector(
                            ".price-per-cup"
                        )?.textContent.trim() || null,

                        regular_price: root.querySelector(
                            ".was-price"
                        )?.textContent.trim() || null,

                        product_url: root.querySelector(
                            ".product-title-container .title a"
                        )?.href || null
                    };
                });

                return results.filter(
                    product => product !== null
                );
            }
        """)

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