import sys
import time
import schedule
import json
sys.path.append('nationslunch/')
from database import MyClient
from database import Spreadsheet
import subprocess
FILE_PATH = 'c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/output/images.jl'
CLIENT_SECRETS = "nationslunch/client_secret.json"

client = MyClient(CLIENT_SECRETS)
sheet = Spreadsheet(client, 'Nationslunch', 0)


    
def job():
    subprocess.run('scrapy runspider nationsspider.py', shell=True,
            cwd="c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/spiders")
    
    url_items={}
    with open(FILE_PATH) as file:
        json_text = file.readlines()

    for line in json_text:
        name = json.loads(line)['name'][0]
        url = json.loads(line)['file_urls'][0]
        url_items[name]=url
    sheet.update_sheet(0,1,list(url_items.keys()))
    sheet.update_sheet(0,2,list(url_items.values())) 
    #print(list(url_items.values()))


schedule.every().day.at("21:00").do(job)



while True:
    schedule.run_pending()
    time.sleep(1)
    

    
