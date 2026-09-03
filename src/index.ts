import * as cheerio from "cheerio";

async function scrape(url: string) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(
      `Request failed: ${response.status} ${response.statusText}`
    );
  }

  const html = await response.text();

  const $ = cheerio.load(html);

  const title = $("title").text().trim();

  console.log({
    url,
    title,
  });
}

scrape("https://www.coles.com.au");