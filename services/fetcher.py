
import json, time
from os import path, mkdir
import time, multiprocessing

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def convert_month(month):
    months = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12",
    }
    return months[month]

def save_data(url):
    try:
        print(f"# INFO: Baixando dados de {url}")
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        raw_name = driver.find_element_by_tag_name('h2').text

        try:
            raw_name = driver.find_element_by_tag_name('h2').text
        except:
            raw_name = ""

        try:
            description = driver.find_element_by_class_name("display-field").text
        except:
            description = ""

        try:
            img_pre = driver.find_element_by_class_name("imgPreview").get_attribute("src")
        except:
            img_pre = ""

        try:
            day = driver.find_element_by_class_name("dayOfMonth").text
            month = convert_month(driver.find_element_by_class_name("month").text)
            year = driver.find_element_by_class_name("calendarDateWindow").find_elements_by_tag_name('div')[3].text
            release_date = f"{year}-{month}-{day}"
        except:
            release_date = ""

        try:
            links = driver.find_element_by_class_name('affiliateList').find_elements_by_tag_name("a")
            amazon_link_uk = links[0].get_attribute("href")
            amazon_link_us = links[1].get_attribute("href")
        except:
            amazon_link_uk = ""
            amazon_link_us = ""

        try:
            index = raw_name.index('(Manga)')
            name = raw_name[:index]
            try:
                words = name.split()[-2:]
                if words[0] == "Volume":
                    volume_num = words[1]
                    index_vol = name.index('Volume')
                    manga = name[:index_vol - 1]
                    if manga[-1:] == ",":
                        manga = manga[:-1]
                elif words[0] == "Part":
                    volume_num = words[1]
                    index_part = name.index('Part')
                    manga = name[:index_part - 1]
                    if manga[-1:] == ",":
                        manga = manga[:-1]
                else:
                    volume_num = -1
                    manga = ""

            except:
                volume_num = -1
        except:
            name = ""
            volume_num = -1
            pass

        data = {
            "raw_name": raw_name,
            "manga": manga,
            "name": name,
            "volume_num": volume_num,
            "description": description,
            "img_pre": img_pre,
            "release_date": release_date,
            "amazon_link_uk": amazon_link_uk,
            "amazon_link_us": amazon_link_us
        }
        with open(f'json_db/{raw_name}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
            print(f"# INFO: Salvando dados de {raw_name}")
    except:
        print("# ERROR: ***********{url}***********")

class Fetcher:
    URL = 'https://otakucalendar.com/us/Search?SearchText=%22%22&searchPastEvents=true&searchPastEvents=false'
    DB_PATH = ""
    _driver = None
    _xpath = []

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Chrome(options=options)

    def run(self):
        print(f"# INFO: Loading Page...")
        self._driver.get(self.URL)
        for _ in range(10):
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        table = self._driver.find_element_by_class_name("listing")
        elements = table.find_elements_by_tag_name("a")
        ulrs = []
        print(f"# INFO: Getting urls...")
        for element in elements[:100]:
            if "(Manga)" in element.text:
                ulrs.append(element.get_attribute("href"))

        with multiprocessing.Pool(processes=5) as pool:
            pool.map(save_data, ulrs)