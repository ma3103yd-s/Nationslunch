import sys
import time
import schedule
import json
sys.path.append('nationslunch/')
from database import MyClient
from database import Spreadsheet
import subprocess
FILE_PATH = 'c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/output/images.jl'
PHONE_FILE_PATH = 'c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/output/phone.jl'
CLIENT_SECRETS = "nationslunch/client_secret.json"

client = MyClient(CLIENT_SECRETS)
sheet = Spreadsheet(client, 'Nationslunch', 0)


    
def menu_job():
    subprocess.run('scrapy runspider nationsspider.py', shell=True,
            cwd="c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/spiders")
    
    url_items={}
    dates = []
    with open(FILE_PATH) as file:
        json_text = file.readlines()

    for line in json_text:
        name = json.loads(line)['name'][0]
        url = json.loads(line)['file_urls'][0]
        dates.append(json.loads(line)['date'][0].strip('\n'));
        url_items[name]=url
    sheet.update_sheet(0,1,list(url_items.keys()))
    sheet.update_sheet(0,2,list(url_items.values()))
    sheet.update_sheet(0,3,dates);
    #print(dates);

def phone_job():
    subprocess.run('scrapy runspider gspider.py', shell=True,
            cwd="c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/spiders")
    
    with open(PHONE_FILE_PATH) as file:
        json_text = file.readlines()
        phone_nbr=[]
        phone_nbr.append(json.loads(json_text[0])['phone_nbr'])
        
    sheet.delete_col(0,4)
    row = sheet.get_row(0,'Göteborg')
    sheet.update_cell(0,row+1, 4, phone_nbr[0]) 
    

schedule.every().day.at("10:00").do(menu_job)
schedule.every().day.at('11:00').do(phone_job)
menu_job()

while True:
    schedule.run_pending()
    time.sleep(1)
    


