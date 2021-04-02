
import json, time
from os import path, mkdir

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Fetcher:
    AMAZON_PRODUCTS = "https://www.amazon.com/s?i=digital-text&k"
    EDITION_TAG = "dbs_s_ks_series_rwt_tkin"
    DB_PATH = ""
    _driver = None
    _xpath = []

    def __init__(self, manga_name):
        self._manga_name = manga_name
        self.DB_PATH = f"json_db/{self._manga_name}"
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Chrome()

        with open("config/data_xpath.json") as json_file:
            self._xpath = json.load(json_file)

    def run(self):
        url = f'{self.AMAZON_PRODUCTS}={self._manga_name}+manga'
        self._list_editions(url)

    def _list_editions(self, manga_url):
        self._driver.get(manga_url)
        time.sleep(15)

        elements = self._driver.find_elements_by_xpath("//a[@href]")
        products_url = [element.get_attribute("href") for element in elements]
        editions_url = list(set([edition for edition in products_url if self.EDITION_TAG in edition]))

        if not path.exists(self.DB_PATH):
            mkdir(self.DB_PATH)

        with open(f"{self.DB_PATH}/editions.json", 'w') as editions:
            data = {}
            data['editions_url'] = editions_url
            json.dump(data, editions)

        self._driver.quit()
        return editions_url
