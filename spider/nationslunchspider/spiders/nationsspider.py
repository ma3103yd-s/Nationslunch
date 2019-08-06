from nationslunchspider.items import NationslunchspiderItem as nlitem
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Response
from scrapy.http import TextResponse
import scrapy
import time
import re



class NationsSpider(scrapy.Spider):
    name = "Nationsspider"
    SCROLL_PAUSE_TIME = 0.5
    start_urls = [
    "https://www.facebook.com/pg/goteborgs/posts/?ref=page_internal",
    "https://www.facebook.com/pg/helsingkrona/posts/?ref=page_internal",
    "https://www.facebook.com/pg/hallandsnation/posts/?ref=page_internal",
    "https://www.facebook.com/pg/lundsnation/posts/?ref=page_internal",
    "https://www.facebook.com/pg/kristianstadsnation/posts/?ref=page_internal",
    "https://www.facebook.com/pg/malmonation/posts/?ref=page_internal",
    "https://www.facebook.com/pg/kalmarnationlund/posts/?ref=page_internal",
    "https://www.facebook.com/pg/sydskanska/posts/?ref=page_internal",
    "https://www.facebook.com/pg/Ostgota/posts/?ref=page_internal",
    ]

    def __init__(self):
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



    def parse(self, response):
        found_photo = False
        self.browser.get(response.url)
        last_height = self.browser.execute_script(
            "return document.body.scrollHeight")
        item = nlitem()
        while(not found_photo):
            el = self.browser.find_elements_by_class_name("_4-u2._4-u8")

            #el = self.browser.find_elements_by_class_name("_5pbx.userContent._3576")
            for e in el:
                # Fix the find_element_by_class_name by selecting from el
                #text_el = e.find_elements_by_class_name("_5pbx.userContent._3576")
                caption = str(e.text)

                if re.search("[Vv]ecka.", caption) or re.search("[Mm]eny.", caption):
                    image_el = self.find_image(e)
                    if not image_el == None:
                        image_class = image_el.find_element_by_class_name("uiScaledImageContainer")
                        image = image_class.find_element_by_css_selector('img')
                        image_url = image.get_attribute('src')
                        item['file_urls'] = [image_url]
                        found_photo = True
                        break


            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(NationsSpider.SCROLL_PAUSE_TIME)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        yield item
