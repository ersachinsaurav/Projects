from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

username = os.getenv('providerUsername')
password = os.getenv('providerPassword')
url = os.getenv('providerUrl')

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/Users/ssaurav/Downloads//'}
chrome_options.add_experimental_option('prefs', prefs)
# chrome_options.add_argument( 'headless' )
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get(url)
driver.find_element('name', 'usernameInput').send_keys(username)
driver.find_element('name', 'passwordInput').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="main-content"]/section/div/form/div[2]/div[1]/div/button').click()
time.sleep(6)
driver.find_element(
    By.CSS_SELECTOR, '#main-content > section > div > ul > li:nth-child(2) > div > div.flex-grow.flex.flex-col.justify-center > span.pt-2 > a').click()
time.sleep(7)
driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/nav/div/div/ul/li[2]/a').click()
driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/nav/div/div/ul/li[2]/div/div/div/ul/li[1]/a').click()
time.sleep(5)
driver.find_element(
    By.XPATH, '//*[@id="root"]/div/div[4]/section/div/div/div/div[2]/div/div/div/div[2]/div/div[3]/div/div[2]/button').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="+izmzszn5h8cMYsf3lKHT3vLgIYgIkKZbSAagQ=="]').click()
time.sleep(6)
driver.close()
print('Invoice Downloaded....')

'''
caUserName = os.getenv('caUsername')
caPassword = os.getenv('caPassword')
caUrl = os.getenv('caUrl')

driver = webdriver.Chrome()
driver.get(caUrl)
driver.maximize_window()

# time.sleep(6)
driver.find_element( 'name', 'ctl00$ContentPlaceHolder1$UsernameTextBox' ).send_keys(caUserName)
driver.find_element( 'name', 'ctl00$ContentPlaceHolder1$PasswordTextBox' ).send_keys(caPassword)
# driver.find_element( 'type', 'submit' )
driver.find_element( By.NAME, 'ctl00$ContentPlaceHolder1$SubmitButton' ).click()
time.sleep(6)

WebDriverWait( driver, 20 ).until( EC.element_to_be_clickable( ( By.ID, 'invoice_acquisition_utility_provider_multiselect' ) ) ).click()
WebDriverWait( driver, 10 ).until( EC.element_to_be_clickable( ( By.ID, 'invoice_acquisition_utility_provider_option_0' ) ) ).click()
WebDriverWait( driver, 20 ).until( EC.element_to_be_clickable( ( By.ID, 'invoice_acquisition_utility_provider_option_302' ) ) ).click()
time.sleep( 5 )

driver.find_element( By.ID, 'js-invoice-acquisition-filter-submit' ).click()
time.sleep(7)
WebDriverWait( driver, 20 ).until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="invoice_acquisition_detail_table"]/tbody/tr[2]/td[11]/a' ) ) ).click()
time.sleep(5)
WebDriverWait( driver, 10 ).until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="utility_bill_account_details"]/div[2]/div[1]/b[2]/dl[6]/dd/div/button' ) ) ).click()
time.sleep(5)
fileUploadElement = driver.find_element( By.NAME, 'acquisition_invoice' )
time.sleep(5)
file_path = "D:\WebRetrieval\Download\Billing.pdf"
fileUploadElement.send_keys(file_path)
driver.find_element(By.XPATH,'//*[@id="upload_acquisition_invoice_frm"]/div/div/input').click()
time.sleep( 5 )
alert = driver.switch_to.alert
alert.accept()
time.sleep( 5 )
print( 'File Uploaded successfully....' )
'''
