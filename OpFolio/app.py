from flask import Flask, redirect, url_for, render_template
from markupsafe import escape
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",stockList=[["MSCI World","20","103,32"],["MSCI EM","10","83,07"]],depotValue=[1003,1000])

if __name__ == "__main__":
    app.run(debug=True)