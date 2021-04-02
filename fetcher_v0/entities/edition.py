import json, time, re

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Edition:
    VOLUME_TAG = "dbs_m_mng_rwt_calw_tkin"
    _driver = None
    _name: str
    _manga_name: str
    _edition_url: str
    _num_volumes: int
    _volumes_url = []


    def __init__(self, manga_name, editions_url):
        self._manga_name = manga_name
        self._edition_url = editions_url

        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Chrome()


    def paginate_volume(self, goto_last_volume, num):
        goto_last_volume.clear()
        goto_last_volume.send_keys(num)
        goto_last_volume.send_keys(u'\ue007')
        time.sleep(3)

        elements = self._driver.find_elements_by_xpath("//a[@href]")
        products_url = [element.get_attribute("href") for element in elements]
        return [volume for volume in products_url if self.VOLUME_TAG in volume]


    def set_volumes_url(self):
        self._driver.get(self._edition_url)
        self._name = self._driver.find_element_by_id("collection-title").text
        print(f"# DEBUG: Edition {self._name} -> Volume URL")

        collection_size = self._driver.find_element_by_id("collection-size").text
        self._num_volumes = int(re.findall(r'\d+', collection_size)[0])

        goto_last_volume = None
        try:
            goto_last_volume = self._driver.find_element_by_id("seriesAsinListGoToId")
        except:
            pass

        if goto_last_volume:
            volumes = []
            for num in range(20, self._num_volumes, 20):
                v_urls = self.paginate_volume(goto_last_volume, num)
                volumes = [v for v in v_urls]
            v_urls = self.paginate_volume(goto_last_volume, self._num_volumes)
            volumes = [v for v in v_urls]
            self._volumes_url = list(set([volume for volume in volumes]))

        else:
            elements = self._driver.find_elements_by_xpath("//a[@href]")
            products_url = [element.get_attribute("href") for element in elements]
            self._volumes_url = list(set([edition for edition in products_url if self.VOLUME_TAG in edition]))

        self._driver.quit()


    def save_json(self):
        if self._num_volumes != len(self._volumes_url):
            print(f"# ERROR[{self._name}]: Missing getting all volumes url.")
            print(f"# ERROR[{self._name}]: Expected {self._num_volumes} and found {len(self._volumes_url)}")

        data = {
            "name" : self._name,
            "manga_name" : self._manga_name,
            "edition_url" : self._edition_url,
            "num_volumes" : self._num_volumes,
            "volumes_url" : self._volumes_url
        }
        with open(f'json_editions/{self._name}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
