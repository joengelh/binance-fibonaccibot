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
from youtubesearchpython import *
import re

#read env vars
load_dotenv()

channel_id = "UCqK_GSMbpiV8spgD3ZGloSw"
playlist = Playlist(playlist_from_channel_id(channel_id))

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

client = Client(apiKey, apiSecret, {'timeout':600})
tickers = client.get_ticker()
print(tickers)
#initiate list to save advice
advice = []

#get possible names of crypto pais
cpl = []
cpl.extend(playlist.videos[0]["title"].split())
for i in range(len(tickers)):
    intermDict = buildPairDict(tickers, i)
    for word in cpl:
        alphanum = ''.join(e for e in word if e.isalnum())
        if "BNB" + alphanum.upper() == intermDict["symbol"]:
            advice.append(intermDict["symbol"])

#print(advice)
