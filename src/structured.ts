import * as cheerio from "cheerio";
// import { readFile } from "node:fs/promises";

async function scrapeStructuredData(url: string) {
//   const html = await readFile("src/local.html", "utf8");
    const response = await fetch(url);
    const html = await response.text();

    const $ = cheerio.load(html);

    const scripts = $('script[type="application/ld+json"]');  // css selector

    console.log("JSON-LD blocks:", scripts.length);

}

scrapeStructuredData("https://books.toscrape.com/");