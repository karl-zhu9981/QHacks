const puppeteer = require("puppeteer");
const fs = require("fs");

module.exports = async id => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://www.conversion-tool.com/audiotomidi/");
  const input = await page.$("#localfile");
  await input.uploadFile(`./downloads/${ id }.wav`);

  await page.click("button.btn.btn-primary.btn-lg.ct-submission-button");
  await page.waitForNavigation();
  fs.unlinkSync(`./downloads/${ id }.wav`);

  const links = await page.$$eval("div.entry-content.clearfix ul li a", el => el.map(e => e.href));
  browser.close();
  return links[1];
}