import pandas as pd
import numpy as np
import seaborn as sns
import yfinance as yf
import matplotlib.pyplot as plt
#%matplotlib inline

class YahooAPI():
    
    def getOneYearClose(symbol):
        ticker = yf.Ticker(symbol)
        df = pd.DataFrame(ticker.history(period="1y"))
        df_close = df["Close"]
        return df_close
    
    #ToDo: Lösung für yield_column.append(0), da Rendite am ersten Tag gleich 0 wäre
    def getOneYearYields(symbol, lg=True):
        ticker = yf.Ticker(symbol)
        df = pd.DataFrame(ticker.history(period="1y"))
        df_close = pd.DataFrame(df["Close"])
        yield_column = []
        yield_column.append(0)
        if (lg == True):
             for i in range(len(df_close)-1):
                yield_column.append(np.log(df["Close"][i+1] / df["Close"][i]))
        else:
             for i in range(len(df_close)-1):
                    yield_column.append((df["Close"][i+1] / df["Close"][i] -1 ))
        df_close["Yields"] = yield_column
        return df_close["Yields"]
       

        
    
    getOneYearYields("AAPL")