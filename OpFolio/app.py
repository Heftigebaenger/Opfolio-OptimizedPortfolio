from calendar import month
from re import S
from flask import Flask, redirect, url_for, render_template, jsonify
import time, json
from flask import request
from stock import Stock 
from alphavantageAPI import AlphavantageAPI
from tradingAPI import TradingApi
from ameriTradeAPI import AmeriTradeAPI
from portfolio import Portfolio
# apikey for alphaventage
apikeyAlpha = "EBYN9X417QJPRW0H"
# apikey for ameritrade
apikeyAmeri = "96I1BNR5FXVTRTMNASI2Z7IPYG07MG9P"

activeAPI = AmeriTradeAPI()
# Get the app form Flask package
app = Flask(__name__)
date = str(int(round(time.time() * 1000)))
print(date);
# Globalvariable for your Depot
# This needs to be replaced by a SQL database
depotwert = 0
kaufwert = 0
depotwertDiff = 0
kaufwertDiff = 0
depotwertDiffPro = 0
kaufwertDiffPro = 0

# Dictionary with Stocks transactions: 
# Key = WKN of the Stock, Value = Array[Name,Quantity,Curr. Value,WKN,Type,Difference,Buy Value]
# This needs to be replaced by a SQL database
stocks = {  'BNTX':["BionTech",20,103.32,"BNTX","Aktie",0.31,101.01],
            'AAPL':["Apple",10,83.07,"AAPL","Aktie",0.1,81.01],
            'BABA':["Alibaba",80,19.41,"BABA","Aktie",0.3,67.04]}

myPortfoli = Portfolio(1)
print(myPortfoli.stockList)

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
    stockValue = []
    stockPercentage = []
    portfolioVolume = 0
    for stock in myPortfoli.stockList:
        currentPrice = activeAPI.getToday(stock[0])["candles"][-1]["close"]
        print(currentPrice)
        portfolioVolume = portfolioVolume + currentPrice*stock[1]
        stockValue.append(currentPrice*stock[1])
    print(stockValue)
    print(portfolioVolume)
    for stock in stockValue:
        stockPercentage.append(stock / portfolioVolume)
    print(stockPercentage)

    stockYield = []
    for stock in myPortfoli.stockList:
        stockData = Stock(stock[0],{},{},{},{},{},{},{},{})
        stockData.today = activeAPI.getToday(stock[0])
        stockData.lastMonth = activeAPI.getLastMonth(stock[0])
        stockData.informations = activeAPI.getInformations(stock[0])
        stockData.today = activeAPI.getToday(stock[0])
        stockData.last6Month = activeAPI.getLast6Month(stock[0])
        stockData.lastYear = activeAPI.getLastYear(stock[0])
        stockData.last5Years = AmeriTradeAPI.getLast5Years(stock[0])
        stockData.companyInfo = AlphavantageAPI.getCompanyOverview(stock[0])
        stockData.last5YearsDaily = AmeriTradeAPI.getLast5YearsDaily(stock[0])
        stockData.calc()
        stockYield.append(stockData.yieldLast5Years)
    print(stockYield)
    
    return render_template("index.html",stockList=stocks,depotValue=[depotwert,kaufwert,depotwertDiff,depotwertDiffPro,kaufwertDiff,kaufwertDiffPro])

# This function is called when open a stock url /stock/...
# Renders the stock.html
@app.route("/stock/<wkn>")
def stockpage(wkn):
    #Renders the stock.html with these arguments: 
    # stock = Array[Name,Quantity,Curr. Value,WKN,Type,Difference,Buy Value]
    return render_template("stock.html")

@app.route("/stock/api/<symbol>", methods=["GET"])
def apidata(symbol):
    activeAPI = AmeriTradeAPI()
    stockData = Stock(symbol,{},{},{},{},{},{},{},{})
    stockData.today = activeAPI.getToday(symbol)
    stockData.lastMonth = activeAPI.getLastMonth(symbol)
    stockData.informations = activeAPI.getInformations(symbol)
    stockData.today = activeAPI.getToday(symbol)
    stockData.last6Month = activeAPI.getLast6Month(symbol)
    stockData.lastYear = activeAPI.getLastYear(symbol)
    stockData.last5Years = AmeriTradeAPI.getLast5Years(symbol)
    stockData.companyInfo = AlphavantageAPI.getCompanyOverview(symbol)
    stockData.last5YearsDaily = AmeriTradeAPI.getLast5YearsDaily(symbol)
    stockData.calc()
   #stockData.calc()
    symbol = request.headers.get("symbol")
    # url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=" + apikey
    return json.dumps(stockData.__dict__)
# Runs the app 










if __name__ == "__main__":
    app.run(debug=True)
