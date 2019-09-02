from flask import Flask
from flask import render_template
from database import MyClient
from database import Spreadsheet

file = "/home/nationsluncharna/nationslunch/Nationslunch/nationslunch/client_secret.json"
client = MyClient(file)
sheet = Spreadsheet(client, 'Nationslunch', 0)


def get_values():
    names = sheet.sheets[0].col_values(1)
    urls = sheet.sheets[0].col_values(2)
    return urls


app =  Flask(__name__, template_folder="/home/nationsluncharna/nationslunch/Nationslunch/templates")


@app.route('/')
def show_images():
    url_items = get_values()
    return render_template("photos.html", variable=url_items)
