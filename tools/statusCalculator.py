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

sumbnb = 0
client = Client(apiKey, apiSecret, {'timeout':600})
tickers = client.get_ticker()
for asset in client.get_account()["balances"]:
    if float(asset["free"]) > 0:
        if asset["asset"] == "BNB":
            sumbnb += float(asset["free"])
        print(asset)
        if asset["asset"] != "ETH":
            for i in range(len(tickers)):
                intermDict = buildPairDict(tickers, i)
                if intermDict["symbol"] == "BNBEUR":
                    bnbEurPrice = intermDict["askPrice"]
                if intermDict["symbol"] == asset["asset"] + "BNB":
                    sumbnb += float(asset["free"]) * float(intermDict["bidPrice"])
sumbnb -= 1.16949939
print(sumbnb, "BNB")
print(sumbnb * bnbEurPrice, "€")
