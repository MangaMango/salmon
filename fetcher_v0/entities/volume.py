import json, time, pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Volume:
    _driver = None
    _name: str
    _edition_name: str
    _volume_url: str
    _amazon_link: str
    _amazon_image_url: str

    def __init__(self):
        options = Options()
        options.add_argument("--headless")

    def _get_amazon_link(self, url, edition_name):
        self._driver = webdriver.Chrome()
        self._edition_name = edition_name
        self._volume_url = url
        cookies = pickle.load(open("cookies.pkl", "rb"))
        self._driver.get(url)
        for cookie in cookies:
            self._driver.add_cookie(cookie)

        self._driver.refresh()
        self._name = self._driver.find_element_by_id("productTitle").text
        img = self._driver.find_element_by_id("ebooksImgBlkFront")
        self._amazon_image_url = img.get_attribute("src")
        self._driver.find_element_by_xpath('//a[@title="Text"]').click()
        time.sleep(2)
        self._amazon_link = self._driver.find_element_by_id("amzn-ss-text-shortlink-textarea").text
        self._save_json()
        self._driver.quit()

    def _save_json(self):
        data = {
            "name" : self._name,
            "volume_url" : self._volume_url,
            "edition_name" : self._edition_name,
            "amazon_link" : self._amazon_link,
            "amazon_image_url" : self._amazon_image_url
        }
        with open(f'json_volumes/{self._name}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)