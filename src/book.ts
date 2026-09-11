import * as cheerio from "cheerio";

async function scrapeBooks() {
  const url = "https://books.toscrape.com/";

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(
      `Request failed: ${response.status} ${response.statusText}`
    );
  }

  const html = await response.text();
  const $ = cheerio.load(html);

  const books = $("article.product_pod");
  console.log("Book cards:", books.length);

  books.each((index, element) => {
    const book = $(element);

    const title = book.find("h3 a").attr("title");
    const price = book.find(".price_color").text().trim();

    console.log({
        title, price
    });
  });
//   console.log("Page title:", $("title").text().trim());
//   console.log("Book cards:", $("article.product_pod").length);
}

scrapeBooks();