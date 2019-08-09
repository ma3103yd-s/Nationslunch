import sys
import time
import schedule
import json
sys.path.append('c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider')
sys.path.append('c:/users/markus/desktop/projects/nationslunch/nationslunch')
from spiders.nationsspider import run_spider
from database import MyClient
from database import Spreadsheet

FILE_PATH = 'c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/output/images.jl'
CLIENT_SECRETS = "nationslunch/client_secret.json"

client = MyClient(CLIENT_SECRETS)
sheet = Spreadsheet(client, 'Nationslunch', 0)

def job():
    run_spider()

    url_items=[]
    with open(FILE_PATH) as file:
        json_text = file.readlines()

    for line in json_text:
        url_items.append(json.loads(line)['file_urls'][0])

    sheet.update_sheet(0, url_items)


job()
