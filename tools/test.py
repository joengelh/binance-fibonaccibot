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

client = Client(apiKey, apiSecret, {'timeout':600})
print(get_exchange_info())
