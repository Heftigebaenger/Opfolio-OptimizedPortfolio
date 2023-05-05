#%%
from logging import error
from pickle import TRUE
from yfinanceAPI import YahooAPI
import numpy as np
import pandas as pd
from math import sqrt
from stock import Stock
import random
import matplotlib.pyplot as plt
from scipy.stats import kstest
from scipy.stats import lognorm
from scipy.optimize import minimize


class Portfolio():
    stockList = []
    id = 0
    def __init__(self,id):
        self.id = id
        #self.loadFromFile()

    def addStock(self,symbol,shares):
        self.stockList.append((symbol,shares))
        f = open("Portfolios/portfolio"+str(self.id)+".txt","a")
        f.write(str(symbol)+":"+str(shares)+"\n")
        f.close()

    def loadFromFile(self):
        if(self.id == 0):
            error("Invalid Portfolio Id")
            return
        f = open("Portfolios/portfolio"+str(self.id)+".txt", "r")
        for line in f:
            splitedList = line.split(":")
            if(len(splitedList) != 2):
                error("Portfolio File:"+str(self.id)+"wrong Format")
                return 
            self.stockList.append((splitedList[0],int(splitedList[1])))
        f.close()

    def removeStock(self,symbol):
        i = 0
        for stock in self.stockList:
            i = i +1
            if(stock[0][0] == symbol):
                break
        f = open("Portfolios/portfolio"+str(self.id)+".txt","r") 
    
    # Die Varianz-Kovarianz Matrix stellt in der diagonale die Varianz der Einzelwerte da
    # In den anderen Feldern stehen die Kovarianzen der jeweiligen Werte (WP1, Wp2), (WP1, WP3) etc
    # Mit Hilfe dieser Methode berechnen wir Opportunity Sets mit n > 2 Anlagen  

    # ToDo. StockList vom Portfolio anpassen für diese Methode
    def VarKovMatrix(self, stocks):
        data_stocks = pd.DataFrame()
        for symbol in stocks:
            data_stocks[symbol]=YahooAPI.getOneYearYields(symbol, lg=True)
        KovMatrix = data_stocks.cov()
        KovMatrix = KovMatrix.multiply(Stock.tradingdays)
        #print("KovMatrix")
        #print(KovMatrix)
        return KovMatrix

    # ToDo: Ist aktuell noch nichts berechnet 
    def CorrMatrix(self,stocks):
        data_stocks = pd.DataFrame()
        for symbol in stocks:
            data_stocks[symbol]=YahooAPI.getOneYearYields(symbol, lg=True)
        CorrMatrix = data_stocks.corr()
        #print("CorrMatrix")
        #print(CorrMatrix)
        return CorrMatrix

    
        

    def multiPortfolio(self):
        stocks = ["SAP","KO","MSFT","DB","DAX"]
        yields = [0.325,-0.021,0.047,-0.043,0.14]
        
        data_stocks = pd.DataFrame()
        for symbol in stocks:
            data_stocks[symbol]=YahooAPI.getOneYearYields(symbol, lg=True)
        #calculate the yield for one year for each stock in data_stocks
        data_stocks = data_stocks.pct_change()
        data_stocks = data_stocks.mean()
        data_stocks = data_stocks * Stock.tradingdays

        print("Data Stocks")
        print(data_stocks)
       
        randomMatrix = np.random.rand(500,len(stocks))
        sumRandomMatrix = np.sum(randomMatrix, axis=1)
        divisionMatix = np.tile(sumRandomMatrix, (len(stocks),1))
        anteilMatrix = randomMatrix / divisionMatix.T
        #print("AnteilMatrix")
        #print(anteilMatrix)
        #yieldsBigMatrix = np.tile(yields, (500,1))
        #print("Yield Matrix")
        #print(yieldsBigMatrix.T)
        portfolioRenditeVector = np.dot(anteilMatrix,yields)
        
        varkovMatrix = np.array(self.VarKovMatrix(stocks))
        
        riskMatrix = np.apply_along_axis(self.multiPortfolioHelper,1,varkovMatrix,anteilMatrix).T
        riskMatrix = np.matmul(riskMatrix, anteilMatrix.T)
        riskVector = np.diagonal(riskMatrix)
        riskVector = np.sqrt(riskVector)
        #print("riskVector")
        #print(riskVector)
        #print(portfolioRenditeVector)
        f = open("risk.txt","w")
        for i in riskVector:
            f.write(str(i)+"\n") 
        p = open("yield.txt","w")
        for i in portfolioRenditeVector: 
            p.write(str(i)+"\n")
        f.close()
        p.close()
        plt.plot(riskVector,portfolioRenditeVector, 'ro', markersize=1)
        varCovMatrix = self.VarKovMatrix(stocks)

        weights = self.optimize_portfolio(varCovMatrix)
        print("Weights")
        print(weights)

        minimumVarianzRendite = np.dot(weights,yields)
        minimumStandartabweichungRisiko = np.sqrt(np.dot(weights.T, np.dot(varCovMatrix, weights)))

        print("Minimum Varianz Rendite")
        print(minimumVarianzRendite)
        print("Minimum Standartabweichung Risiko")
        print(minimumStandartabweichungRisiko)

        

    def portfolioVariance(self, weight, varcov):
        return np.dot(weight.T, np.dot(varcov, weight))
        

    def optimize_portfolio(self, varCovMatrix):
        constraints = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
        bounds = tuple((0,1) for x in range(varCovMatrix.shape[0]))
        num_assets = varCovMatrix.shape[0]
        args = (varCovMatrix)
        initial_guess = num_assets * [1. / num_assets,]
        result = minimize(self.portfolioVariance, initial_guess, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x
    



        
    



        


        


    def multiPortfolioHelper(self,varkovMatrixVector,anteilMatrix):
        print(varkovMatrixVector)
        return np.dot(anteilMatrix,varkovMatrixVector)


    #Relative Häufigkeiten Einzelwerte 
    def distributionYields(self):
        stocks = ["SAP","BNTX"]
        Yields = [0.2]
        WPIntervallAll = []
        SigmaInterval = 3.25
        AnzahlIntervalle = 14
        Left_Range = 0
        Right_Range = 0
        stockTest = 0

        fig, axes = plt.subplots(1, 2)
        #For Schleife zum erzeugen der Intervalle (X-Achse Gaußverteilung)
        for i in range(len(stocks)):
  
            oneYearYields = YahooAPI.getOneYearYields(stocks[i], lg=False)
            print(oneYearYields)
            oneYearYields.hist(ax = axes[i],legend=True,bins = 20)




           
       
    
        #For Schleife zum erstellen der relativen Häufigkeiten (Yields)
        #for stock in stocks:

    


portfolioOne = Portfolio(1)
portfolioOne.multiPortfolio()
plt.show()




# %%
