import scrapy
import time
import re
import sys
sys.path.append('../')
from items import NationslunchspiderItem as nlitem
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from scrapy.http import Response
import subprocess

class NationsSpider(scrapy.Spider):
    name = "Nationsspider"
    nationer = {
            "https://www.facebook.com/goteborgs/posts/?ref=page_internal":"Göteborg",
            "https://www.facebook.com/helsingkrona/posts/?ref=page_internal":"Helsingkrona",
            "https://www.facebook.com/hallandsnation/posts/?ref=page_internal":"Hallands",
            "https://www.facebook.com/lundsnation/posts/?ref=page_internal":"Lunds",
            "https://www.facebook.com/kristianstadsnation/posts/?ref=page_internal":"Kristianstads",
            "https://www.facebook.com/malmonation/posts/?ref=page_internal":"Malmo",
            "https://www.facebook.com/kalmarnationlund/posts/?ref=page_internal":"Kalmar",
            "https://www.facebook.com/sydskanska/posts/?ref=page_internal":"Sydskånska",
            "https://www.facebook.com/Ostgota/posts/?ref=page_internal":"Östgöta",
            }



    SCROLL_PAUSE_TIME = 0.5
    start_urls = list(nationer.keys())
   
    correct_images = {
        "https://www.facebook.com/goteborgs/posts/?ref=page_internal":['281','500'],
        "https://www.facebook.com/helsingkrona/posts/?ref=page_internal":['281', '500'],
        "https://www.facebook.com/hallandsnation/posts/?ref=page_internal":['354','500'],
        "https://www.facebook.com/lundsnation/posts/?ref=page_internal":['352', '500'],
        "https://www.facebook.com/kristianstadsnation/posts/?ref=page_internal":['501','281'],
        "https://www.facebook.com/malmonation/posts/?ref=page_internal":['500','625'],
        "https://www.facebook.com/kalmarnationlund/posts/?ref=page_internal":['500','387'],
        "https://www.facebook.com/sydskanska/posts/?ref=page_internal":['344','500'],
        "https://www.facebook.com/Ostgota/posts/?ref=page_internal":['500','500'],
    }

    def __init__(self):
        #options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()


    def find_image(self, parent_element):
        different_images = ["_2a2q._65sr", "_1ktf"]
        for image in different_images:
            try:
                sub_element = parent_element.find_element_by_class_name(image)
            except Exception as e:
                pass
            else:
                return sub_element



    def inner(self, url, item):
        el = self.browser.find_elements_by_class_name("_4-u2._4-u8")


        for e in el:

            caption = str(e.text)
            image_el = self.find_image(e)
            if not image_el == None:
                image_class = image_el.find_element_by_class_name("uiScaledImageContainer")
                image = image_class.find_element_by_css_selector('img')
                dimensions=[
                            image.get_attribute('width'),
                            image.get_attribute('height'),
                            ]
                print(dimensions)
                if NationsSpider.correct_images[url] == dimensions:
                    print(caption)
                        #print(correct_images[url])
                    image_url = image.get_attribute('src')
                    item['file_urls'] = [image_url]
                    
                    return True



    def parse(self, response):
        found_photo = False
        self.browser.get(response.url)

        last_height = self.browser.execute_script(
            "return document.body.scrollHeight")
        item = nlitem()
        while(not found_photo):

            found_photo = self.inner(response.url, item)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(NationsSpider.SCROLL_PAUSE_TIME)
            #self.browser.implicitly_wait(NationsSpider.SCROLL_PAUSE_TIME)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            last_height = new_height
        item['name'] = [NationsSpider.nationer[response.url]]
        yield item


