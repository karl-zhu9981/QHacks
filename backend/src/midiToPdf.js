const fs = require("fs");
const puppeteer = require("puppeteer");
const downloadImage = require("./downloadImage");
const makePdf = require("./makePdf");

module.exports = id => {
  return new Promise(async (resolve, reject) => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto("https://solmire.com/miditosheetmusic");
    const input = await page.$("input");
    await input.uploadFile(`./downloads/${ id }.midi`);
    const button = await page.$("input[type=image]");
    button.press("Enter");

    await page.waitForSelector("img.sheet", { visible: true, timeout: 0 });
    fs.unlinkSync(`./downloads/${ id }.midi`);

    const urls = await page.$$eval("img.sheet", sheets => sheets.map(sheet => sheet.src));

    let promises = [];
    for (let i = 0; i < urls.length; i++) {
      promises.push(downloadImage(urls[i], i));
    }

    browser.close();
    Promise.allSettled(promises).then(() => resolve(makePdf(id)));
    promises = null;
  });
}