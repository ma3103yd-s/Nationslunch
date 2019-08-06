
from flask import Flask
from flask import render_template
import json
from pyvirtualdisplay import Display

app =  Flask(__name__, template_folder="/home/nationsluncharna/nationslunch/templates")


@app.route('/')
def show_images():
    file_name="/home/nationsluncharna/nationslunch/spider/nationslunchspider/output/images.jl"
    with open(file_name, 'r') as file:
        json_text=file.readlines()

    url_items = []
    for line in json_text:
        url_items.append(json.loads(line)['file_urls'][0])
        print(type(url_items[0]))
    return render_template("photos.html", url=url_items)

if __name__ == '__main__':
    app.run()
