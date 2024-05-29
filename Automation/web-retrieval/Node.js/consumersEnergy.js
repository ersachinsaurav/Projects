const puppeteer = require('puppeteer');
require('dotenv').config();

const caUrl = process.env.caUrl;
const caUsername = process.env.caUsername;
const caPassword = process.env.caPassword;
const providerUrl = process.env.providerUrl;
const providerUsername = process.env.providerUsername;
const providerPassword = process.env.providerPassword;

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: null,
    args: ['--start-maximized'],
  });

  // console.log(process.env);
  // return;

  // Login to CA
  await loginIntoCA(browser, caUrl, caUsername, caPassword);

  // Login to Consumers Energy
  await loginIntoConsumersEnergy(
    browser,
    providerUrl,
    providerUsername,
    providerPassword
  );
})();

async function loginIntoCA(browser, url, caUsername, caPassword) {
  try {
    const caPage = await browser.newPage();
    await caPage.goto(url);

    await caPage.type('#login_div > div:nth-child(2) > input', caUsername);
    await caPage.type('#login_div > div:nth-child(4) > input', caPassword);

    await caPage.click('#signin-submit');
    await caPage.waitForNetworkIdle();

    await caPage.click('#invoice_acquisition_utility_provider_multiselect');
    await caPage.click('#invoice_acquisition_utility_provider_option_0');

    await caPage.click('#invoice_acquisition_utility_provider_multiselect');
    await caPage.type('#option_filter_text', ' Consumers Energy', {
      delay: 250,
    });

    await caPage.evaluate(() => {
      const options = document.querySelectorAll('.binded-label.item-found'); // Target specific class combination
      for (const option of options) {
        const label = option.querySelector('label');
        if (label && label.textContent.trim() === 'Consumers Energy') {
          const checkbox = option.querySelector('input[type="checkbox"]');
          if (checkbox) {
            checkbox.checked = true;
            break; // Exit loop after finding and checking the checkbox
          }
        }
      }
    });

    // Submit the form
    await caPage.click('#js-invoice-acquisition-filter-submit');

    await caPage.waitForNetworkIdle();
    await caPage.click(
      '#invoice_acquisition_detail_table > tbody > tr.noClick.bRow > td:nth-child(11) > a'
    );
    await caPage.waitForNetworkIdle();
  } catch (error) {
    console.log(error);
  }
}

async function loginIntoConsumersEnergy(
  browser,
  providerUrl,
  providerUsername,
  providerPassword
) {
  try {
    const providerPage = await browser.newPage();
    await providerPage.goto(providerUrl);
    await providerPage.waitForNetworkIdle();

    await providerPage.type('#input28', providerUsername);
    await providerPage.click('#form20 > div.o-form-button-bar > input');
    await providerPage.waitForNetworkIdle();

    await providerPage.click(
      '#form53 > div.authenticator-verify-list.authenticator-list > div > div:nth-child(2) > div.authenticator-description > div.authenticator-button > a'
    );

    await providerPage.waitForNetworkIdle();

    await providerPage.type('#input93', providerPassword);
    await providerPage.click('#form85 > div.o-form-button-bar > input');
    await providerPage.waitForNetworkIdle();

    // Moving to download invoice pdf
    await providerPage.click(
      'body > div:nth-child(8) > header > div.wp-header-container.static-nav.wp-lx-navigation.d-none.d-lg-table.alert-closed > div > div > div.header-nav-container > nav > ul > li:nth-child(1) > div > button'
    );
    await providerPage.click(
      'body > div:nth-child(8) > header > div.wp-header-container.static-nav.wp-lx-navigation.d-none.d-lg-table.alert-closed > div > div > div.header-nav-container > nav > ul > li:nth-child(1) > div > div.login-popover.dropdown-menu.show > div:nth-child(3) > ul > li:nth-child(14) > a'
    );

    await providerPage.waitForNetworkIdle();

    await providerPage.select('#selectedAccount', '100077863999');
    await providerPage.waitForNetworkIdle();

    await providerPage.select('#SortPayments', 'DueDate Desc');

    await providerPage.click(
      '#tblBills tbody tr:nth-child(2) td:nth-child(4) a'
    );
    // Logout..
    await providerPage.click(
      'div.header-nav-container > nav > ul > li:nth-child(1) > div > button'
    );
    await providerPage.click(
      'div.header-nav-container > nav > ul > li:nth-child(1) > div > div.login-popover.dropdown-menu.show > div.single-account-log.col-md-5 > div.balanceFrame > div.row.remove-ie.d-none.d-lg-flex > div.col-sm-12.single-account > a.float-right.logout.event-ga-tag'
    );

    await providerPage.waitForNetworkIdle();
    await providerPage.close();
    await browser.close();
  } catch (error) {
    console.log(error);
  }
}
