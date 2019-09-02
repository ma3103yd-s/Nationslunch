# This module fetches the values from the spreadsheets to avoid generating too many api calls

from database import MyClient
from database import Spreadsheet

file = "/home/nationsluncharna/nationslunch/Nationslunch/nationslunch/client_secret.json"
client = MyClient(file)
sheet = Spreadsheet(client, 'Nationslunch', 0)

names = sheet.sheets[0].col_values(1)
urls = sheet.sheets[0].col_values(2)
file = "urls.csv"
with open(file,'w') as f:
    for i in range(len(names)):
        f.write(f"{names[i]}, {urls[i]}\n")


