import puppeteerExtra from 'puppeteer-extra';
import userPrefs from 'puppeteer-extra-plugin-user-preferences';
import dotenv from 'dotenv';

dotenv.config();

let browser;
let page;

const credentials = [
  {
    username: process.env.txuUsername,
    password: process.env.txuPassword,
  },
];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

puppeteerExtra.use(
  userPrefs({
    userPrefs: {
      download: {
        prompt_for_download: false,
      },
      plugins: {
        always_open_pdf_externally: true,
      },
    },
  })
);

async function init(url) {
  console.log('init');
  browser = await puppeteerExtra.launch({
    headless: false,
    defaultViewport: null,
    args: ['--start-maximized'],
  });
  page = await browser.newPage();
  await page.goto(url);
  console.log('Page loaded');
}

async function loginTXUEnergy(username, password) {
  try {
    console.log('login TXUEnegry:');
    await page.focus('#Username');
    await page.keyboard.type(username);
    console.log('Username typed');

    await page.focus('#Password');
    await page.keyboard.type(password);
    console.log('Password typed');

    const searchForm = await page.$('#frmAuth');
    await searchForm.evaluate((searchForm) => searchForm.submit());
    console.log('Form has been submitted.');

    await page.waitForNavigation({ waitUntil: 'networkidle2' });
    console.log('TXU login successfully.');
  } catch (error) {
    console.log('We got some erors: ');
    console.log(error);
  }
}

async function downloadBill() {
  try {
    const linkSelector = '#loadPdf';
    console.log('Wait for link selector to load');
    await page.waitForSelector(linkSelector);
    console.log('Now we will click on link to download bill');
    await page.click(linkSelector);
    console.log('Awaiting for bill to download');
    await page.waitForNetworkIdle();
    console.log('Bill is downloaded successfully.');
  } catch (error) {
    console.log('We got some erors: ');
    console.log(error);
  }
}

async function logoutTXUEnergy() {
  try {
    console.log('logout TXUEnegry:');

    await page.click('#user_signout');
    console.log('Clicked on signout');

    await page.waitForNetworkIdle();
    console.log('TXU logout successfully.');
  } catch (error) {
    console.log('We got some erors: ');
    console.log(error);
  }
}

async function execute() {
  const url = process.env.txuUrl;

  await init(url);

  for (let credential of credentials) {
    console.log('Wait for 5 secs to login TXUEnergy.');
    sleep(5000);
    await loginTXUEnergy(credential.username, credential.password);
    console.log('Wait for 5 secs to download bill.');
    sleep(5000);
    console.log('Wait is complete.');
    await downloadBill();
    console.log('Wait for 5 secs to logout.');
    sleep(5000);
    console.log('Wait is complete.');
    await logoutTXUEnergy();
  }

  await browser.close();
  console.log('browser is closed.');
}

execute();
