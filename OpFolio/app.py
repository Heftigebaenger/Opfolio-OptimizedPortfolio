from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)
depotwert = 0
kaufwert = 0
depotwertDiff = 0
kaufwertDiff = 0
depotwertDiffPro = 0
kaufwertDiffPro = 0
stocks = [  ["MSCI World",20,103.32,"R92E92","ETF",0.31,101.01],
            ["MSCI EM",10,83.07,"A30E59","ETF",0.1,81.01],
            ["Alibaba",80,19.41,"K10594","Aktie",0.3,67.04]]

def calcDepotwert():
    calc = 0
    for stock in stocks:
        calc = calc + stock[1]*stock[2]
    return calc

def calcKaufwert():
    calc = 0   
    for stock in stocks:
        calc = calc + stock[1]*stock[6]
    return calc
    

def calcKaufwertDiff():
    return round(depotwert -kaufwert,2)

def calcKaufwertDiffPro():
    return round((kaufwertDiff/kaufwert)*100,2)


depotwert = calcDepotwert()
kaufwert = calcKaufwert()
kaufwertDiff= calcKaufwertDiff()
kaufwertDiffPro = calcKaufwertDiffPro()
@app.route("/")
def index():
    return render_template("index.html",stockList=stocks,depotValue=[depotwert,kaufwert,depotwertDiff,depotwertDiffPro,kaufwertDiff,kaufwertDiffPro])

if __name__ == "__main__":
    app.run(debug=True)