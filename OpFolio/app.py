from flask import Flask, redirect, url_for, render_template
# Get the app form Flask package
app = Flask(__name__)

# Globalvariable for your Depot

depotwert = 0
kaufwert = 0
depotwertDiff = 0
kaufwertDiff = 0
depotwertDiffPro = 0
kaufwertDiffPro = 0

# Dictionary with Stocks transactions: 
# Key = WKN of the Stock, Value = Array[Name,Quantity,Curr. Value,WKN,Type,Difference,Buy Value]
stocks = {  'R92E92':["MSCI World",20,103.32,"R92E92","ETF",0.31,101.01],
            'A30E59':["MSCI EM",10,83.07,"A30E59","ETF",0.1,81.01],
            'K10594':["Alibaba",80,19.41,"K10594","Aktie",0.3,67.04]}

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

# Runs the app 
if __name__ == "__main__":
    app.run(debug=True)