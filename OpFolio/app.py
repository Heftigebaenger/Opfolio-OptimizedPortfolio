from calendar import month
from cmath import sqrt
from distutils.log import error
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
print(date)
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
        if(len(activeAPI.getToday(stock[0])["candles"]) == 0):
            error("No Candle Data ")
        print(activeAPI.getToday(stock[0])["candles"])
        currentPrice = activeAPI.getInformations(stock[0])["lastPrice"]
        print(currentPrice)
        portfolioVolume = portfolioVolume + currentPrice*stock[1]
        stockValue.append(currentPrice*stock[1])
    print(stockValue)
    print(portfolioVolume)
    for stock in stockValue:
        stockPercentage.append(stock / portfolioVolume)
    

    stockYield = []
    stockData = []
    k = 0
    print(myPortfoli.stockList)
    for stock in myPortfoli.stockList:
        stockData.append(Stock(stock[0],{},{},{},{},{},{},{},{}))
        stockData[k].today = activeAPI.getToday(stock[0])
        stockData[k].lastMonth = activeAPI.getLastMonth(stock[0])
        stockData[k].informations = activeAPI.getInformations(stock[0])
        stockData[k].today = activeAPI.getToday(stock[0])
        stockData[k].last6Month = activeAPI.getLast6Month(stock[0])
        stockData[k].lastYear = activeAPI.getLastYear(stock[0])
        stockData[k].last5Years = AmeriTradeAPI.getLast5Years(stock[0])
        stockData[k].companyInfo = AlphavantageAPI.getCompanyOverview(stock[0])
        stockData[k].last5YearsDaily = AmeriTradeAPI.getLast5YearsDaily(stock[0])
        stockData[k].calc()
        stockYield.append(stockData[k].yieldForEachYear[0])
        k = k+1
    print("Aktien Anteile: "+ str(stockPercentage))
    print("Aktien Rendite: "+ str(stockYield))
    
    portfolioYield = 0
    portfolioStandart = 0
    for i in range(len(stockPercentage)):
        print(stockData[i])
        print(stockData[i].standartDeviOneYear)
        portfolioStandart = portfolioStandart + stockPercentage[i]*stockData[i].standartDeviOneYear
        portfolioYield = portfolioYield**2 + (stockPercentage[i]*stockYield[i])**2
    Stock.calcCorrelationCoefficient(stockData[0],stockData[1])
    print("Portfolio Rendite: "+ str(portfolioYield))
    print("Portfolio Standart: "+ str(portfolioStandart))
    corr = Stock.calcCorrelationCoefficient(stockData[0],stockData[1])
    
    risk = stockPercentage[0]**2 * stockData[0].standartDeviOneYear**2 + stockPercentage[1]**2 * stockData[1].standartDeviOneYear**2 + 2*stockPercentage[0]*stockPercentage[1]* stockData[0].standartDeviOneYear * stockData[1].standartDeviOneYear * corr
    risk = sqrt(risk)
    print(str(risk))
    return render_template("index.html",stockList=stocks,depotValue=[depotwert,kaufwert,depotwertDiff,depotwertDiffPro,kaufwertDiff,kaufwertDiffPro])

# This function is called when open a stock url /stock/...
# Renders the stock.html
@app.route("/stock/<wkn>")
def stockpage(wkn):
    #Renders the stock.html with these arguments: 
    # stock = Array[Name,Quantity,Curr. Value,WKN,Type,Difference,Buy Value]
    return render_template("stock.html")

@app.route("/risk")
def riskpage():
    return render_template("risk.html")


@app.route("/risk/api/<symbolOne>/<symbolTwo>", methods=["GET"])
def riskApiRequest(symbolOne,symbolTwo): 
    # This function calculates the risk between two stocks given by the symbols
    riskStocks = [symbolOne,symbolTwo]
    stockYield = []
    stockData = []
    k = 0
    print(riskStocks)
    # Get the data for the stocks
    for stock in riskStocks:
        stockData.append(Stock(stock[0],{},{},{},{},{},{},{},{}))
        stockData[k].today = activeAPI.getToday(stock)
        stockData[k].lastMonth = activeAPI.getLastMonth(stock)
        stockData[k].informations = activeAPI.getInformations(stock)
        stockData[k].today = activeAPI.getToday(stock)
        stockData[k].last6Month = activeAPI.getLast6Month(stock)
        stockData[k].lastYear = activeAPI.getLastYear(stock)
        stockData[k].last5Years = AmeriTradeAPI.getLast5Years(stock)
        stockData[k].companyInfo = AlphavantageAPI.getCompanyOverview(stock)
        stockData[k].last5YearsDaily = AmeriTradeAPI.getLast5YearsDaily(stock)
        stockData[k].calc()
        stockYield.append(stockData[k].yieldForEachYear[0])
        k = k+1
    print("Aktien Rendite: "+ str(stockYield))


    portfolioYield = 0
    stockPercentage = [0,0]
    corr = Stock.calcCorrelationCoefficient(stockData[0],stockData[1])
    effCurveArray= []
    # Calculate the risk for every possible combination of the stocks
    for i in range(0,101):
        stockPercentage[0] = (i)*0.01
        stockPercentage[1] = (100-i)*0.01
        portfolioYield = stockPercentage[0]*stockYield[0] + stockPercentage[1]*stockYield[1]
        risk = stockPercentage[0]**2 * stockData[0].standartDeviOneYear**2 + stockPercentage[1]**2 * stockData[1].standartDeviOneYear**2 + 2*stockPercentage[0]*stockPercentage[1]* stockData[0].standartDeviOneYear * stockData[1].standartDeviOneYear * corr
        print(risk)
        risk = sqrt(risk)
    
        effCurveArray.append((portfolioYield,risk.real))
    print(effCurveArray)

    return json.dumps({"effCurveArray" :effCurveArray,"corr": corr})


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
    # url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol="+symbol+"&apikey=" + apikey
    return json.dumps(stockData.__dict__)
# Runs the app 










if __name__ == "__main__":
    app.run(debug=True)
