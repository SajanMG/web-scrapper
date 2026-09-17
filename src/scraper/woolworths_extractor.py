from playwright.sync_api import Page


def extract_woolworths_raw_products(page: Page):
    return page.evaluate("""
        () => {
            const tiles = document.querySelectorAll("wc-product-tile");

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
                    )?.href || null,

                    available: root.querySelector(
                        ".product-tile-unavailable-tag"
                    ) === null
                };
            });

            const failedTile = Array.from(tiles).find(tile => {
                if (!tile.shadowRoot) {
                    return false;
                }

                const name = tile.shadowRoot.querySelector(
                    ".product-title-container .title a"
                )?.textContent.trim();

                return name === "Woolworths 12 Extra Large Free Range Eggs 700g";
            });

            if (failedTile) {
                console.log("FAILED TILE HTML:");
                console.log(failedTile.shadowRoot.innerHTML);
            }

            return results.filter(product => product !== null);
        }
    """)