import pandas as pd
import numpy as np
import seaborn as sns
import yfinance as yf
import matplotlib.pyplot as plt
#%matplotlib inline

class YahooAPI():
    
    def getOneYearClose(symbol):
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1y")
        df_close = df["Close"]
        print(df_close)
    getOneYearClose("MSFT")
