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
    
    REFRESH_TIME = 60

    start_urls = ["https://www.facebook.com/goteborgs/posts/?ref=page_internal"]

    def __init__(self):

        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

    def parse(self, response):
        self.browser.get(response.url)
        
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
            driver.refresh()
            time.sleep(GSpider.REFRESH_TIME)
            yield item



               

        
