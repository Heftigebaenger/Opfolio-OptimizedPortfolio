from flask import Flask, redirect, url_for, render_template, jsonify
import requests
import time, json
from flask import request
# Get the app form Flask package
# apikey for alphaventage
apikeyAlpha = "EBYN9X417QJPRW0H"
# apikey for ameritrade
apikeyAmeri = "96I1BNR5FXVTRTMNASI2Z7IPYG07MG9P"
app = Flask(__name__)
date = str(int(round(time.time() * 1000)))
# Globalvariable for your Depot

depotwert = 0
kaufwert = 0
depotwertDiff = 0
kaufwertDiff = 0
depotwertDiffPro = 0
kaufwertDiffPro = 0

# Dictionary with Stocks transactions: 
# Key = WKN of the Stock, Value = Array[Name,Quantity,Curr. Value,WKN,Type,Difference,Buy Value]
stocks = {  'BNTX':["BionTech",20,103.32,"BNTX","Aktie",0.31,101.01],
            'AAPL':["Apple",10,83.07,"AAPL","Aktie",0.1,81.01],
            'BABA':["Alibaba",80,19.41,"BABA","Aktie",0.3,67.04]}

# Functions to Calculate the Depotvalues based on the transactions
def calcDepotwert():
    calc = 0
    for key in stocks:
        calc = calc + stocks[key][1]*stocks[key][2]
        print()
    return calc

def calcKaufwert():
    calc = 0   
    for key in stocks:
        calc = calc + stocks[key][1]*stocks[key][6]
        print(stocks[key])
    return calc
    
def calcKaufwertDiff():
    return round(depotwert -kaufwert,2)

def calcKaufwertDiffPro():
    return round((kaufwertDiff/kaufwert)*100,2)
# end of Depotfunktions

# Set the Globalvalues to the actuall values
depotwert = calcDepotwert()
kaufwert = calcKaufwert()
kaufwertDiff= calcKaufwertDiff()
kaufwertDiffPro = calcKaufwertDiffPro()

# This function is called when open the url /
# Renders the index.html
@app.route("/")
def index():
    #Renders the stock.html with these arguments: 
    # stockList = List of stock tansactions
    # depotValue = Array[RealDepotValue, BuyDepotValue, DepotValueDiff to Yesterday Absolute, DepotValueDiff to Yesterday in %,BuyDepotValueDiff absolute,BuyDepotValueDiff in %]
    return render_template("index.html",stockList=stocks,depotValue=[depotwert,kaufwert,depotwertDiff,depotwertDiffPro,kaufwertDiff,kaufwertDiffPro])

# This function is called when open a stock url /stock/...
# Renders the stock.html
@app.route("/stock/<wkn>")
def stockpage(wkn):
    #Renders the stock.html with these arguments: 
    # stock = Array[Name,Quantity,Curr. Value,WKN,Type,Difference,Buy Value]
    return render_template("stock.html",stock=stocks[wkn])

@app.route("/stock/api/<symbol>", methods=["GET"])
def apidata(symbol):
    apiStockData = {
        "info":{},
        "lastMonth":{},
        "quotes": {}
    }
    # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=&apikey='+apikey
    # url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=apple&apikey=" + apikey

    symbol = request.headers.get("symbol")
    # url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=" + apikey
    apiStockData["info"] = apiAmeriFundamental(symbol)
    apiStockData["lastMonth"] = apiAmeriLastMonthData(symbol)
    apiStockData["quotes"] = apiAmeriQuotes(symbol)
    return json.dumps(apiStockData)
# Runs the app 

def apiAmeriFundamental(symbol):
    url = "https://api.tdameritrade.com/v1/instruments?apikey="+apikeyAmeri+"&symbol="+symbol+"&projection=fundamental"
    r = requests.get(url)
    data = r.json()
    data = data[symbol]
    return data

def apiAmeriLastMonthData(symbol):
    url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory?apikey="+apikeyAmeri+"&periodType=month&period=1&frequencyType=daily&frequency=1&endDate="+date+"&needExtendedHoursData=true"
    r = requests.get(url)
    data = r.json()
    return data

def apiAmeriQuotes(symbol):
    url = "https://api.tdameritrade.com/v1/marketdata/"+symbol+"/quotes?apikey=" + apikeyAmeri
    r = requests.get(url)
    data = r.json()
    data = data[symbol]
    return data


if __name__ == "__main__":
    app.run(debug=True)