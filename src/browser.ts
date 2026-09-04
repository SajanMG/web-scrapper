import { chromium } from "playwright";

async function scrapePage(url: string) {
  const browser = await chromium.launch({
    headless: false,
  });

  const page = await browser.newPage();

  await page.goto(url);

  const title = await page.title();

  console.log({
    url,
    title,
  });

  await browser.close();
}

scrapePage("https://www.coles.com.au");