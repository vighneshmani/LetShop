from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import time
from selenium.common.exceptions import NoSuchElementException



class AmazonBot(object):

    def __init__(self, items):
        self.amazon_url = 'https://www.amazon.in/'
        self.items = items
        self.profile = webdriver.FirefoxProfile()
        self.options = Options()
        self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                        options=self.options)
        self.driver.get(self.amazon_url)

    def search_items(self):

        urls = []
        prices = []
        names = []

        for item in self.items:
            wait = WebDriverWait(self.driver, 10)
            print("Searching for ", item)
            self.driver.get(self.amazon_url)
            search_input = self.driver.find_element_by_id("twotabsearchtextbox")
            search_input.send_keys(item)

            time.sleep(2)

            search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
            search_button.click()

            time.sleep(2)
            first_result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-badge-label")))
            first_result.click()

            url = self.driver.current_url

            # print(first_result)
            # print(price)
            # print(name)
            price = self.get_product_price(url)
            name = self.get_product_name(url)

            prices.append(price)
            urls.append(url)
            names.append(name)

            print(name)
            print(price)
            print(url)

            time.sleep(2)

        return prices, urls, names

    def get_product_price(self, url):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)
        product_price = ""
        try:
            product_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="priceblock_ourprice"]'))).text

        except:

            pass

        try:
            product_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="priceblock_dealprice"]'))).text
        except:
            pass

        if product_price is None:
            product_price = "Not available"

        else:
            non_decimal = re.compile(r'[^\d.]+')
            product_price = non_decimal.sub('', product_price)

        return product_price

    def get_product_name(self, url):

        wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)
        product_name = ""
        try:
            product_name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productTitle"]'))).text
        except:
            pass

        if product_name is None:
            product_name = "Not available"
        return product_name

    def close_session(self):

        self.driver.close()

#item = ['salt']
#amazon_bot = AmazonBot(item)
#amazon_bot.search_items()
