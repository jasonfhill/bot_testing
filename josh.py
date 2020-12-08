import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

options = Options()
# Set a window size
options.add_argument("window-size=1400,600")


# Randomize the user agent
# When you connect to a web site you send a "user-agent" to identify yourself.
# You don't want this to be "selenium" because that is obviously a bot.
# This code randomizes that so it will be:
#     Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36
#     Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36
#     Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36
#   etc..
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options.add_argument(f'user-agent={user_agent}')


def availabilitycheck():
    r = requests.get('https://feature.com/products.json')
    products = json.loads((r.text))['products']

    for product in products:
        #print(product['title'])
        productname = product['title']

        if productname == 'Nike Adapt Auto Max Black White':

            producturl = 'https://feature.com/products/' + product['handle']
            #print(producturl)
            return producturl

    return False


# Link to product

# I commented out your driver since I'm on linux. Does my method work for you though?
# driver = webdriver.Chrome(executable_path=r'C:\Users\Josh\Desktop\chromedriver.exe')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://feature.com/products/nike-adapt-auto-max-black-white')
#
# #Click Size, Add To Cart, and Checkout
driver.find_element_by_xpath('//div[@data-value="10"]').click()
driver.find_element_by_xpath('//button[@class="primary-btn add-to-cart"]').click()

# The main issue was that you were trying to click this immediately, it just wasn't ready yet
# The easy option is a dumb wait like I have commented below. It waits 20 seconds. That might be 10 seconds too long,
# or not long enough.
# driver.implicitly_wait(20)

# This is an EXCPLICIT wait. It is a much better way to go since you tell it exactly what to wait for. Below I have it
# set to wait for the XPATH we want to click on (or give up in 30 seconds)
WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((
    By.XPATH, '//div[@id="ajax-cart"]/div/div/section/footer/a')))

# That explicit wait above finished so now we should be clear to click this thing
driver.find_element_by_xpath('//div[@id="ajax-cart"]/div/div/section/footer/a').click()

# We clicked above, so now we have to wait again. Now we're waiting for the email field though.
WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((
    By.XPATH, '//input[@placeholder="Email"]')))

# Contact info and Shipping info
driver.find_element_by_xpath('//input[@placeholder="Email"]').send_keys('example@gmail.com')
driver.find_element_by_xpath('//input[@placeholder="First name"]').send_keys('First Name')
driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys('Last Name')
driver.find_element_by_xpath('//input[@placeholder="Company (optional)"]').send_keys('Company (optional)')
driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys('Address')
driver.find_element_by_xpath('//input[@placeholder="Apartment, suite, etc. (optional)"]').send_keys('Apartment, suite, etc. (optional)')