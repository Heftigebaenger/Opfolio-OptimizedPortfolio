
from logging import error
from yfinanceAPI import YahooAPI
import numpy as np
import pandas as pd
from math import sqrt
from stock import Stock
import random
import matplotlib.pyplot as plt
from scipy.stats import kstest
from scipy.stats import lognorm


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
        print(KovMatrix)
        return KovMatrix

    # ToDo: Ist aktuell noch nichts berechnet 
    def CorrMatrix(self,stocks):
        data_stocks = pd.DataFrame()
        for symbol in stocks:
            data_stocks[symbol]=YahooAPI.getOneYearYields(symbol, lg=True)
        CorrMatrix = data_stocks.corr()
        print(CorrMatrix)
        return CorrMatrix


    def multiPortfolio(self):
        stocks = ["KO","BNTX","MSFT","DB"]
        yields = [0.25,0.3,0.4,-0.13]
        #rndm_nr = np.empty()
        #port_shares = np.empty(0)
        #i = 0
        #while i < len(stocks):
         #   np.append(rndm_nr, random.random())
          #  i += 1
        #print(rndm_nr)


        randomMatrix = np.random.rand(500,len(stocks))
        sumRandomMatrix = np.sum(randomMatrix, axis=1)
        divisionMatix = np.tile(sumRandomMatrix, (len(stocks),1))
        anteilMatrix = randomMatrix / divisionMatix.T

        #yieldsBigMatrix = np.tile(yields, (500,1))
        #print("Yield Matrix")
        #print(yieldsBigMatrix.T)
        portfolioRenditeVector = np.dot(anteilMatrix,yields)
        
        varkovMatrix = np.array(self.VarKovMatrix(stocks))
        
        riskMatrix = np.apply_along_axis(self.multiPortfolioHelper,1,varkovMatrix,anteilMatrix).T
        riskMatrix = np.matmul(riskMatrix, anteilMatrix.T)
        riskVector = np.diagonal(riskMatrix)
        riskVector = np.sqrt(riskVector)
        print("riskVector")
        print(riskVector)
        print(portfolioRenditeVector)
        f = open("risk.txt","w")
        for i in riskVector:
            f.write(str(i)+"\n") 
        p = open("yield.txt","w")
        for i in portfolioRenditeVector: 
            p.write(str(i)+"\n")
        f.close()
        p.close()


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
        #For Schleife zum erzeugen der Intervalle (X-Achse Gaußverteilung)
        for stock in stocks:
            i = 0
            oneYearYields = np.array(YahooAPI.getOneYearYields(stock, lg=False))
            result = kstest(oneYearYields, "norm")
            oneYearStanDevi = np.std(oneYearYields) * sqrt(Stock.tradingdays)
            Left_Range = Yields[0] - SigmaInterval * oneYearStanDevi
            Right_Range = Yields[0] + SigmaInterval * oneYearStanDevi
            WPTemp = np.array([Left_Range])
            while i <= AnzahlIntervalle:
                InterSeize = Left_Range + i * (Right_Range - Left_Range) / AnzahlIntervalle
                WPTemp = np.append(WPTemp, InterSeize)
                i+= 1
            WPIntervallAll.append(WPTemp)
            print(result)
       
    
        #For Schleife zum erstellen der relativen Häufigkeiten (Yields)
        #for stock in stocks:




portfolioOne = Portfolio(1)
portfolioOne.distributionYields()

  







    
        