from pandas_datareader import data, wb
import pandas as pd
import numpy as np 
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import cufflinks as cf
%matplotlib inline 

#Setting up the environment
sns.set_style('whitegrid')
cf.go_offline()

#Setting up range for Bank Stocks Date
start = datetime.datetime(2006,1,1)
end = datetime.datetime(2016,1,1)

#Creating DataFrame for Each banks
#Bank of America; ticker symbol: 'BAC'
BAC = data.DataReader("BAC", 'yahoo', start, end)
#City Group; ticker symbol: 'C'
C = data.DataReader("C", 'yahoo', start, end)
# Goldman Sachs; ticker symbol: 'GS'
GS = data.DataReader("GS", 'yahoo', start, end)
#JP Morgan Chase; ticker symbol: 'JPM'
JPM = data.DataReader("JPM", 'yahoo', start, end)
#Morgan Stanley; ticker symbol: 'MS'
MS = data.DataReader("MS", 'yahoo', start, end)
#Wells Fargo; ticker symbol: 'WFC'
WFC = data.DataReader("WFC", 'yahoo', start, end)

#Creating a list of tickers
tickers = ['BAC','C','GS','JPM','MS','WFC']

#Merging all the Bank Stock data into a Single DataFrame
bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], axis = 1, keys = tickers)

bank_stocks.columns.names = ['Bank Tickers', 'Stock Info']
bank_stocks.head(5)

#Max Close price for each bank throughout the time period
bank_stocks.xs(key = 'Close', axis = 1, level = 'Stock Info').max()

returns = pd.DataFrame()

for ticker in tickers:
    returns[ticker+' Return'] = bank_stocks[ticker]['Close'].pct_change()
returns.head(5) 

sns.pairplot(returns[1:])

#worst drop (4 of them on inaugration day)
returns.idxmin() 

# Best Single Day Gain
# citigroup stock split in May 2011, but also JPM day after inauguration.
returns.idxmax()

returns.std() #city group is the riskiest

returns.loc['2015-01-01':'2015-12-31'].std() # Very similar risk profiles, but Morgan Stanley or BofA

#A distplot using seaborn of the 2015 returns for Morgan Stanley
sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], color='red', bins=100)

#A distplot using seaborn of the 2008 returns for CitiGroup 
sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Return'], color='yellow',bins=100)

# Create a line plot showing Close price for each bank for the entire index of time
for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4), label=tick)
plt.legend()

#same thing using .xs()
bank_stocks.xs(key='Close', axis = 1, level = 'Stock Info').plot()

#Interactive Graph using plotly
bank_stocks.xs(key='Close', axis = 1, level = 'Stock Info').iplot()

#Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008
plt.figure(figsize=(12,6))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()

#Create a heatmap of the correlation between the stocks Close Price.
sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

#Cluster map
sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(), annot = True)

#Interactive HeatMap
close_corr = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
close_corr.iplot(kind='heatmap',colorscale='rdylbu')

#Use .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.
BAC[['Open', 'High', 'Low', 'Close']].loc['2015-01-01':'2016-01-01'].iplot(kind='candle')

# Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.
MS['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='sma',periods=[13,21,55],title='Simple Moving Averages')

#Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015
BAC['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='boll')