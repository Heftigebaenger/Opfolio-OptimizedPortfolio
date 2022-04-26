



from logging import error, raiseExceptions
from math import sqrt
from statistics import variance
from time import time
<<<<<<< HEAD
from datetime import datetime
from typing import Final, final

# Stock Class to uniform Stockdata
=======


>>>>>>> b29bb43c4622431c8b0337ee0ee4f44eae54612d
class Stock():
    tradingdays: Final = 253
    #Basic Information
    symbol = ""
    informations = {}
<<<<<<< HEAD
    companyInfo = {}
    
    #Stock price data
    today = {}
    lastMonth = {}
    last6Month = {}
    lastYear = {}
    last5Years = {}
    last5YearsDaily = {}

    #Calculated Data
    dailyYieldAverageYearOne = 0
    averageYield = 0
    varianzOneYear = 0
    standartDeviOneYear = 0
    yieldMonthly = []
    yieldForEachYear = []
    yieldLast5Years = 0
    last5YearsDailyYields = []

    def __init__(self,symbol,informations,lastMonth,today,last6Month,lastYear,companyInfo,last5Years,last5YearsDaily):
=======
    lastYear = {}
    companyInfo = {}
    last5Years = {}
    yieldLast5Years = {}
    standartDeviation = 0
    averageYield = 0
    varianz = 0
    standartDevi = 0

    def __init__(self,symbol,informations,lastMonth,today,last6Month,lastYear, companyInfo,last5Years):
>>>>>>> b29bb43c4622431c8b0337ee0ee4f44eae54612d
        self.symbol = symbol
        self.informations = informations
        self.lastMonth = lastMonth
        self.today = today
        self.last6Month = last6Month
        self.lastYear = lastYear
        self.companyInfo = companyInfo
        self.last5Years = last5Years
<<<<<<< HEAD
        self.yieldForEachYear = [0,0,0,0,0]
        self.yields = []
        self.yieldMonthly = []
        self.last5YearsDaily = last5YearsDaily
        self.last5YearsDailyYields = []

    def calc(self):
        self.yieldLast5Years = self.yieldForTwoDays(0,self.tradingdays*5)
        for i in range(5):
            self.yieldForEachYear[i] = self.yieldForTwoDays(self.tradingdays*i,self.tradingdays*(i+1))
        self.averageYield = self.calcAverageYield(self.yieldForEachYear)
        self.last5YearsDailyYields = self.calcDailyYields(0,5* self.tradingdays)
        self.dailyYieldAverageOneYear = self.calcAverageYield(self.last5YearsDailyYields[0:self.tradingdays])
        self.varianzOneYear = self.calcVarianz(0,self.tradingdays,self.dailyYieldAverageOneYear)
        self.standartDevi = self.calcStandartDevi(self.varianzOneYear)


    def calcDailyYields(self,start,end):
        dailyYields = []
        if(start > end or start < 0):
            error("Start is not Valid")
        if(end > len(self.last5YearsDaily["candles"])):
            end = len(self.last5YearsDaily["candles"]) -1
        for i in range(start,end):
           dailyYields.append(self.yieldForTwoDays(i,i+1))
        return dailyYields
     
    # Calculates the yield for two given Days  
    # 0 = Today,  365 = One Year ago
    def yieldForTwoDays(self,dateOne, dateTwo):
        oldDate = 0
        newDate = 0
        #Check which date comes first
        if(dateOne < dateTwo): 
            oldDate = dateTwo
            newDate = dateOne
        else:
            oldDate = dateOne
            newDate = dateTwo
        if(oldDate > len(self.last5YearsDaily["candles"])):
            oldDate = len(self.last5YearsDaily["candles"])-1
 
        oldDate = len(self.last5YearsDaily["candles"]) - oldDate -1 
        newDate = len(self.last5YearsDaily["candles"]) - newDate -1 
        print("NewDate =" + str(newDate))
        self.printCandleData(oldDate)
        self.printCandleData(newDate)
        return (self.last5YearsDaily["candles"][newDate]["close"] - self.last5YearsDaily["candles"][oldDate]["close"]) / self.last5YearsDaily["candles"][oldDate]["close"]

    def printCandleData(self,index):
        date = self.last5YearsDaily["candles"][index]["datetime"]
        price = str(self.last5YearsDaily["candles"][index]["close"])
        date = datetime.fromtimestamp(date/1000);
        print("Start:")
        print("Price:"+price+"Date:"+ datetime.strftime(date,"%Y-%m-%d"));


    def calcVarianz(self,start,end,average):
        if(start > end or start < 0):
            error("Start is not Valid")
        if(end > len(self.last5YearsDaily["candles"])):
            end = len(self.last5YearsDaily["candles"]) - 1
        sum = 0
        for i in range(start,end):
            sum = sum + (self.last5YearsDailyYields[i] - average)**2
           #print(sum)
        sum = sum
        return sum

    def calcStandartDevi(self,varianz):
        if(varianz <= 0):
            error("Varianz = 0")
        return sqrt(varianz)


    def calcAverageYield(self,arrayOfYields):
=======
        self.yields = []
    def calc(self):

        self.yields = self.calcYields(60)
        self.averageYield = self.calcAverageYield(self.yields[1])
        self.varianz = self.calcVarianz()
        self.standartDevi = self.calcStandartDevi()

    def calcVarianz(self):
        if len(self.yields[1]) <= 0:
            error("No AverageYields")
        sum = 0
        for yields in self.yields[1]:
            sum = sum + (yields - self.averageYield)**2
        sum = sum / len(self.yields[1])
        return sum

    def calcStandartDevi(self):
        if(self.varianz <= 0):
            error("Varianz = 0")
        return sqrt(self.varianz)

    def calcYields(self,months):
        if(months < 12):
            error("calcYields: Less then 6 Months")
        years = int(months / 12)
        print("Years:")
        print(years)
        lastMonthIndex = len(self.last5Years["candles"]) - 1
        averageMonthlyYield = []
        averageYearlyYield = []
        for year in range(years):
            startMonthIndex = lastMonthIndex - year * 12
            endMonthIndex = startMonthIndex - 12
            averageMonthlyYieldForOneYear = self.calcMonthlyYieldAverage(startMonthIndex,endMonthIndex, self.last5Years["candles"])
            averageMonthlyYield.append(averageMonthlyYieldForOneYear)
            averageYearlyYield.append((1+averageMonthlyYieldForOneYear)**12-1)
            print(averageMonthlyYield)
        return [averageMonthlyYield,averageYearlyYield]

        

    def calcMonthlyYieldAverage(self, startIndex, endIndex, candleArray):
        if(startIndex < 0):
            error("calcMonthly: startIndex < 0")
        if(endIndex > startIndex or endIndex < 0):
            error("calcMonthly: endIndex wrong")
        monthlyYields = []
        print(endIndex)
        while (startIndex > endIndex and startIndex >0):
            print("StartIndex:")
            print(startIndex)
            yieldForOneMonth = (candleArray[startIndex]["close"] - candleArray[startIndex -1]["close"]) / candleArray[startIndex - 1]["close"]
            monthlyYields.append(yieldForOneMonth)
            startIndex = startIndex - 1 
        print("Monthly Yields")
        print (monthlyYields)
        return self.calcAverageYield(monthlyYields)


    def calcYieldMonthlytoYear(self):
        self.yieldLast5Years 



    def calcAverageYield(self, arrayOfYields):
>>>>>>> b29bb43c4622431c8b0337ee0ee4f44eae54612d
        averageYield = 0
        for yields in arrayOfYields:
            averageYield = averageYield + yields
        averageYield = averageYield / len(arrayOfYields)
<<<<<<< HEAD
        print("Length of Avrage Array: "+str(len(arrayOfYields)))
=======
>>>>>>> b29bb43c4622431c8b0337ee0ee4f44eae54612d
        return averageYield
