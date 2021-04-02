import json, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Manga:
    AMAZON_PRODUCTS = "https://www.amazon.com/s?i=digital-text&k"
    EDITION_TAG = "dbs_s_ks_series_rwt_tkin"
    _driver = None
    _name: str
    _manga_url: str
    _editions_url = []


    def __init__(self, name):
        self._name = name
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Chrome()


    def set_editions_url(self):
        print(f"# DEBUG: Mangas {self._name} -> Editions URL")
        url = f'{self.AMAZON_PRODUCTS}={self._name}+manga'
        self._manga_url = url
        self._driver.get(url)

        elements = self._driver.find_elements_by_xpath("//a[@href]")
        products_url = [element.get_attribute("href") for element in elements]
        self._editions_url = list(set([edition for edition in products_url if self.EDITION_TAG in edition]))
        self._driver.quit()


    def save_json(self):
        data = {
            "name" : self._name,
            "manga_url" : self._manga_url,
            "editions_url" : self._editions_url
        }
        with open(f'json_mangas/{self._name}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
