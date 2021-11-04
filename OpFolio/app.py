from flask import Flask, redirect, url_for, render_template
from markupsafe import escape
app = Flask(__name__)

@app.route("/<name>")
def index(name):
    return render_template("index.html", content=name)

