const puppeteer = require("puppeteer");
const downloadImage = require("./downloadImage");
const makePdf = require("./makePdf");

module.exports = async id => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://solmire.com/miditosheetmusic");
  const input = await page.$("input");
  await input.uploadFile(`./downloads/${ id }.midi`);
  const button = await page.$("input[type=image]");
  button.press("Enter");

  await page.waitForSelector("img.sheet", { visible: true, timeout: 0 });

  const urls = await page.$$eval("img.sheet", sheets => sheets.map(sheet => sheet.src));

  let promises = [];
  for (let i = 0; i < urls.length; i++) {
    promises.push(downloadImage(urls[i], i));
  }

  Promise.allSettled(promises).then(() => makePdf(id));
  promises = null;
  browser.close();
}