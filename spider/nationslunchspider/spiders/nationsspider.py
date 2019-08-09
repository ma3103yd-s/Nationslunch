import scrapy
import time
import re
import datetime
from datetime import timedelta
from items import NationslunchspiderItem as nlitem
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from scrapy.http import Response
from scrapy.http import TextResponse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

date = datetime.datetime.now()
time_diff = timedelta(days=1)
month = date.strftime("%A")
#day = int(unformatted_date.strftime("%d"))
max_date = date + time_diff
min_date = date-time_diff
days = [min_date.day, date.day,max_date.day]
months = [min_date.strftime("%B"), date.strftime("%B"), max_date.strftime("%B")]
if months[0]==months[1]:
    del months[0]

#correct_date = "{}{}[{}{}{}]. ".format(months[0],months[1], days[0], days[1], days[2])
correct_date = "{} [{}{}{}{}{}].".format("June",2,3,4,5,6)

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
    correct_images = {
        "https://www.facebook.com/goteborgs/posts/?ref=page_internal":['281','500'],
        "https://www.facebook.com/helsingkrona/posts/?ref=page_internal":['281', '500'],
        "https://www.facebook.com/hallandsnation/posts/?ref=page_internal":['354','500'],
        "https://www.facebook.com/lundsnation/posts/?ref=page_internal":['352', '500'],
        "https://www.facebook.com/kristianstadsnation/posts/?ref=page_internal":['500','280'],
        "https://www.facebook.com/malmonation/posts/?ref=page_internal":['500','625'],
        "https://www.facebook.com/kalmarnationlund/posts/?ref=page_internal":['500','500'],
        "https://www.facebook.com/sydskanska/posts/?ref=page_internal":['308','500'],
        "https://www.facebook.com/Ostgota/posts/?ref=page_internal":['500','500'],
    }

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



    def inner(self, url, item):
        el = self.browser.find_elements_by_class_name("_4-u2._4-u8")


        for e in el:

            caption = str(e.text)
            if re.search("[Vv]ecka.", caption) or re.search("[Mm]eny.", caption):

                image_el = self.find_image(e)
                if not image_el == None:
                    image_class = image_el.find_element_by_class_name("uiScaledImageContainer")
                    image = image_class.find_element_by_css_selector('img')
                    dimensions=[
                                image.get_attribute('width'),
                                image.get_attribute('height'),
                                ]
                    #print(dimensions)
                    if NationsSpider.correct_images[url] == dimensions:
                        print(correct_date)
                        print(caption)
                        if re.search(correct_date, caption):
                            image_url = image.get_attribute('src')
                            item['file_urls'] = [image_url]
                            return 0
                        self.browser.refresh()
                        return 1


    def parse(self, response):
        found_photo = False
        self.browser.get(response.url)
        print(correct_date)
        last_height = self.browser.execute_script(
            "return document.body.scrollHeight")
        item = nlitem()
        while(not found_photo):

            if not self.inner(response.url, item): found_photo = True
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(NationsSpider.SCROLL_PAUSE_TIME)
            #self.browser.implicitly_wait(NationsSpider.SCROLL_PAUSE_TIME)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            last_height = new_height
        yield item

# import this to run spider
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(NationsSpider)
    process.start()
