#import modules
import json
from binance.client import Client
import sys
import os
import itertools
from dotenv import load_dotenv
import schedule
import time
from envs import env

#import classes from ./ folder
import postgresdbAccess
import tradingEngineAccess
import validationAccess

with open('databaseColumns.json') as file:
    cols = json.load(file)

#read env vars
load_dotenv()

try:
    apiSecret=env('apiSecret')
    apiKey=env('apiKey')
    dbTable=env('dbTable')
    baseCurrency=env('baseCurrency')
except KeyError:
    print("No env variables set.")
    sys.exit(1)

#initiate connection to database
def initiateTable():
    postgres = postgresdbAccess.postgresAccess()
    postgres.tableCreate(cols)
    postgres.databaseClose()
    print("SUCCESS: initialteTable()")

def buildPairDict(tickers, i):
    columns = {}
    columns['symbol'] = tickers[i]['symbol']
    columns['priceChange'] = float(tickers[i]['priceChange'])
    columns['priceChangePercent'] = float(tickers[i]['priceChangePercent'])
    columns['weightedAvgPrice'] = float(tickers[i]['weightedAvgPrice'])
    columns['prevClosePrice'] = float(tickers[i]['prevClosePrice'])
    columns['lastPrice'] = float(tickers[i]['lastPrice'])
    columns['lastQty'] = float(tickers[i]['lastQty'])
    columns['bidPrice'] = float(tickers[i]['bidPrice'])
    columns['bidQty'] = float(tickers[i]['bidQty'])
    columns['askPrice'] = float(tickers[i]['askPrice'])
    columns['askQty'] = float(tickers[i]['askQty'])
    columns['askQty'] = float(tickers[i]['askQty'])
    columns['openPrice'] = float(tickers[i]['openPrice'])
    columns['highPrice'] = float(tickers[i]['highPrice'])
    columns['lowPrice'] = float(tickers[i]['lowPrice'])
    columns['volume'] = float(tickers[i]['volume'])
    columns['quoteVolume'] = float(tickers[i]['quoteVolume'])
    return columns

def crawl():
    #initiate own classes
    postgres = postgresdbAccess.postgresAccess()
    trader = tradingEngineAccess.tradingAccess()
    test = validationAccess.liveAccess()
    #connect to binance
    client = Client(apiKey, apiSecret, {'timeout':600})
    #wait for api to not die
    time.sleep(1)
    #get current market data
    tickers = client.get_ticker()
    #get counts
    countLen = postgres.sqlQuery("SELECT count(*) FROM " + dbTable +
    " WHERE time < NOW() - INTERVAL '24 hours';")
    countOpen = postgres.sqlQuery("SELECT count(*)" +
    " FROM " + dbTable + " WHERE" +
    " resultpercent IS NULL" +
    " AND takeprofit IS NOT NULL;")
    for i in range(len(tickers)):
        intermDict = buildPairDict(tickers, i)
        #dont write data when not usable
        if (intermDict['askPrice'] <= 0 or
            1.015 <= intermDict['lowPrice'] / intermDict['highPrice'] >= 0.985 or
            "UP" in intermDict['symbol'] or
            "DOWN" in intermDict['symbol'] or
            not intermDict['symbol'].endswith(baseCurrency)):
            continue
        #write intermDict to database
        postgres.insertRow(intermDict)
        #and check if enough data has been gathered
        if countLen[0][0] > 0:
            #run caluclation
            trader.runCalculation(intermDict)
    #check if any trades meet the conditions to be closed yet
    if countOpen[0][0] > 0:
        test.validate()
    #close database connection
    postgres.databaseClose()

#create table once on startup, if not exists
initiateTable()

#write price ticker to database every full minute
schedule.every(1).minutes.do(crawl)

#repeat
while True:
    schedule.run_pending()
    time.sleep(1)
