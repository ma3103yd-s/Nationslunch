from flask import Flask
from flask import render_template
from database import MyClient
from database import Spreadsheet

file = "/home/nationsluncharna/nationslunch/Nationslunch/nationslunch/urls.csv"



def get_values():
    names = []
    urls = []
    with open(file, 'r') as f:
        for line in f:
            content = line.split(',')
            names.append(content[0])
            urls.append(content[1])
    return names, urls


app =  Flask(__name__, template_folder="/home/nationsluncharna/nationslunch/Nationslunch/templates")


@app.route('/')
def show_images():
    url_items = get_values()
    return render_template("photos.html", variable=url_items)
