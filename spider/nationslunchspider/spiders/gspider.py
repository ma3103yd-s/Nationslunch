import scrapy
import subprocess
import re
import time
import sys
sys.path.append('../')
import datetime
from items import GSpiderItem as phoneitem
from selenium import webdriver


class GSpider(scrapy.Spider):
    name = "gspider"
    
    SCROLL_PAUSE_TIME = 0.5

    start_urls = ["https://www.facebook.com/goteborgs/posts/?ref=page_internal"]

    def __init__(self):

        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

    def parse(self, response):
        self.browser.get(response.url)
        
        last_height = self.browser.execute_script(
                "return document.body.scrollHeight")
        item = phoneitem()
        found_nbr = False
        while not found_nbr:
            text_element = self.browser.find_elements_by_class_name("_4-u2._4-u8")
            for e in text_element:
                caption = str(e.text)
                nbr_match  = re.search(r"((\+46)|0)([\d]{9})|(\d\d\d)(\s\d\d){3}", caption)
                date_match = re.search(r"[012345678]\s?([Tt]im)", caption)
                if nbr_match and date_match:
                    item['phone_nbr'] = nbr_match.group(0)
                    found_nbr = True
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(GSpider.SCROLL_PAUSE_TIME)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            last_height = new_height
            yield item



               

        
