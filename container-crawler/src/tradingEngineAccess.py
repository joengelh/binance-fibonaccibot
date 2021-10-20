#import modules
import json
from binance.client import Client
import pandas as pd
import os
from envs import env
import time
import statistics
import numpy as np
from scipy.stats import kurtosis, skew

#import classes from ./ folder
import postgresdbAccess

class tradingAccess:
    def __init__(self):
        #read fibonacci retracements  from json
        with open('fibLvl.json') as file:
            self.fibLvl = json.load(file)
        #read if live trading is enabled
        try:
            self.liveTrading=env("liveTrading", 'False').lower() in ('true', '1', 't')
            self.liveVolume=env("liveVolume")
            self.dbTable=env("dbTable")
            self.baseCurrency=env('baseCurrency')
            apiSecret=env('apiSecret')
            apiKey=env('apiKey')
        except KeyError:
            print("No env variables set.")
            sys.exit(1)
        #connect to binance to get current balance
        self.client = Client(apiKey, apiSecret, {'timeout':600})

    def openTrade(self, fib, i, large, cor, tick, statisticsTools):
        if self.liveTrading == True:
            #wait a bit because otherwise api error
            time.sleep(0.01)
            #get assets available before buy
            assetsBefore = float(self.client.get_asset_balance(asset=self.baseCurrency)['free'])
            #skip rest of function if funds not sufficient
            if assetsBefore <= float(self.liveVolume) * 1.1:
                return
            #buy
            self.client.order_market_buy(symbol = tick['symbol'], quoteOrderQty = self.liveVolume)
            #get assets available after buy after waiting 5 seconds
            time.sleep(5)
            assetsAfter = float(self.client.get_asset_balance(asset=self.baseCurrency)['free'])
            #calculate price
            positionCost = assetsBefore - assetsAfter
        else:
            positionCost = 0
        #write the advice
        sql = ("UPDATE " + self.dbTable + " SET " +
            " takeProfit = '" + str(fib[3][i+4]) +
            "', stopLoss = '" + str(fib[2][i-1]) +
            "', corValue = '" + str(cor) +
            "', startId = '" + str(large[0].min()) +
            "', midId = '" + str(large[0].max()) +
            "', fibLevel = '" + str(fib[0][i]) +
            "', positionCost = '" + str(positionCost) +
            "', stDev = '" + str(statisticsTools["stDev"]) +
            "', kurtosis = '" + str(statisticsTools["kurtosis"]) +
            "', skew = '" + str(statisticsTools["skew"]) +
            "' WHERE id IN(SELECT max(id) FROM " + self.dbTable + ");")
        self.postgres.sqlUpdate(sql)

    def corConsistency(self,scale,tick):
        sql = ("SELECT id, askprice, time FROM " + self.dbTable + 
            " WHERE symbol LIKE '" + tick['symbol'] + 
            "' AND time > NOW() - INTERVAL '" + str(scale) + " hours';")
        largeData = pd.DataFrame(self.postgres.sqlQuery(sql))
        largeData[0] = pd.to_numeric(largeData[0])
        largeData[1] = pd.to_numeric(largeData[1])
        corValue = largeData[0].corr(largeData[1])
        return corValue

    def runCalculation(self, tick):
        self.postgres = postgresdbAccess.postgresAccess()
        sql = ("SELECT id, askprice FROM " + self.dbTable + 
            " WHERE symbol LIKE '" + tick['symbol'] + 
            "' AND time > NOW() - INTERVAL '24 hours';")
        largeData = pd.DataFrame(self.postgres.sqlQuery(sql))
        if len(largeData) > 0:    
            #convert columns id and askprice to float
            largeData = largeData.apply(pd.to_numeric, errors='coerce', downcast='float')
            #calculate diff
            diff = largeData[1].max() - largeData[1].min()
            # calculate fibRetracements
            fibRetracement = pd.DataFrame(self.fibLvl)
            maxAsk = largeData[1].max()
            for lvl in fibRetracement:
                fibRetracement[1] =  maxAsk - diff * fibRetracement[0]
                fibRetracement[2] = fibRetracement[1] * 0.9995
                fibRetracement[3] = fibRetracement[1] * 1.0005
            #see of currently an open trade exists
            sql = ("SELECT count(*) FROM " + self.dbTable + 
                    """ WHERE takeprofit is not null and resultpercent is null and 
                    symbol like '""" + tick['symbol'] + "';")
            #get correlation of id and price
            corValue = largeData[0].corr(largeData[1])
            #get statistical parameters
            statisticsTools = {}
            statisticsTools["stDev"] = statistics.stdev(largeData[1])
            statisticsTools["skew"] = skew(largeData[1])
            statisticsTools["kurtosis"] = kurtosis(largeData[1])
            #if no open trade for symbol exists and price in between 7th fiblvl
            for i in [7]:
                if (int(self.postgres.sqlQuery(sql)[0][0]) == 0 and
                    float(tick["priceChangePercent"] >= 0 and
                    corValue >= 0 and
                    statisticsTools["skew"] <= 0 and
                    statisticsTools["kurtosis"] <= 0 and
                float(tick['askPrice']) < fibRetracement[3][i] and
                float(tick['askPrice']) > fibRetracement[2][i]):
                    self.openTrade(fibRetracement, i, largeData, corValue, tick, statisticsTools)
        self.postgres.databaseClose()
