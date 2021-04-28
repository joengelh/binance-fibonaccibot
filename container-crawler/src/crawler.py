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
import timescaledbAccess
import tradingEngineAccess

with open('databaseColumns.json') as file:
    cols = json.load(file)

#read env vars
load_dotenv()

try:
    apiSecret=env('apiSecret')
    apiKey=env('apiKey')
except KeyError:
    print("No env variables set.")
    sys.exit(1)

#initiate connection to database
def initiateTable():
    timescale = timescaledbAccess.timescaleAccess()
    timescale.tableCreate(cols)
    timescale.databaseClose()
    print("SUCCESS: initialteTable()")

def crawl():
    timescale = timescaledbAccess.timescaleAccess()
    trader = tradingEngineAccess.tradingAccess()
    client = Client(apiKey, apiSecret, {'timeout':600})
    tickers = client.get_ticker()
    #get count to determine if lengh is sufficient
    count = timescale.sqlQuery("SELECT count(*) FROM table001 " +
    " WHERE time > NOW() - INTERVAL '12 hours'" + 
    " and time < NOW() - INTERVAL '11 hours';")
    for i in range(len(tickers)):
        intermDict = {}
        intermDict['askPrice'] = float(tickers[i]['askPrice'])
        intermDict['symbol'] = tickers[i]['symbol']
        #filter for only coins relevant for the bot
        if (intermDict['symbol'].endswith('BNB') and
           len(intermDict['symbol']) < 11 and
           intermDict['askPrice'] > 0):
            timescale.insertRow(intermDict)
            if count[0][0] > 0:
                trader.runCalculation(intermDict)
    timescale.databaseClose()

#create table once on startup, if not exists
initiateTable()

#write price ticker to database every full minute
schedule.every().minute.at(":00").do(crawl)
schedule.every().minute.at(":20").do(crawl)
schedule.every().minute.at(":40").do(crawl)

#repeat
while True:
    schedule.run_pending()
    time.sleep(1)
