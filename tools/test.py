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

sumbnb = 0
client = Client(apiKey, apiSecret, {'timeout':600})
tickers = client.get_ticker()
for asset in client.get_account()["balances"]:
    if float(asset["free"]) > 0:
        print(asset)
        if asset["asset"] != "BNBETH":
            pass
            sumbnb += asset["free"] * tickers[ 
print(sumbnb)
