import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

search_url = "https://www.google.com/search?as_st=y&as_q={0}&as_epq=&as_oq=&as_eq=&imgsz=m&imgar=s&imgcolor=&imgtype=photo&cr=&as_sitesearch=&as_filetype=png&tbs=&udm=2"

class ImageDownloader:
    def __init__(self, word):
        self.cuvant = word
        clear_word = self.clear_diacritics(word)
        print(clear_word)
        self.url = search_url.format(clear_word)

    def __get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def clear_diacritics(self, word):
        return word.replace('\u0103', 'a').replace('\u0219', 's').replace('\u021b', 't').replace('\u00e2', 'a')
    
    def download(self):
        driver = self.__get_driver()
        driver.get(self.url)

        try:
            accpt = driver.find_element(By.XPATH, '//*[@id="L2AGLb"]/div')
            driver.execute_script('arguments[0].click()', accpt)
        except Exception:
            pass
        time.sleep(2)

        img_xpath = "//*[@id=\"rso\"]/div/div/div[1]/div/div/div[{0}]/div[2]"
        locations = [1,2,3,8,15]    
        pictures = []
        for loc in locations:
            try:
                pictures += [driver.find_element(By.XPATH, img_xpath.format(loc))]
            except Exception:
                continue

        if not os.path.isdir("images"):
            os.mkdir("images")

        for i in range(len(pictures)):
            with open(os.path.join("images", f"{self.cuvant}_{i:>03}.png"), 'wb') as f:
                f.write(pictures[i].screenshot_as_png)

def load_words(fname):
    words = []
    with open(fname, 'r', encoding="utf-8") as f:
        for ln in f.readlines():
            words += [ln.strip()]
    return words

words = load_words("words_1.txt")
for word in words:
    dld = ImageDownloader(word)
    dld.download()
 