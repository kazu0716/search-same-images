# -*- coding: utf-8 -*-
import os,sys
import glob

from flask import Flask, render_template
from lib.search_images import SearchImages

app = Flask(__name__)
search_images=SearchImages

@app.route("/")
def search_images():
    result = {
        "exact_matches": [],
        "partial_matches": []
    }
    path="./static/img/search_images/*.png"
    search_list = glob.glob(path, recursive=True)
    for image_file in search_list:
        result = search_images(image_file)
    return render_template("index.html", result=result)

def main():
    app.config['DEBUG'] = True
    app.run()

if __name__ == "__main__":
    main()
