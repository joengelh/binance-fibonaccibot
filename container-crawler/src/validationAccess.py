#import modules
import json
import pandas as pd
from binance.client import Client
from envs import env
import time
import re

#import classes from ./ folder
import postgresdbAccess

#read fibonacci retracements  from json
with open('fibLvl.json') as file:
    fibLvl = json.load(file)

class liveAccess:
    def __init__(self):
        try:
            self.liveVolume=env("liveVolume")
            apiSecret=env('apiSecret')
            apiKey=env('apiKey')
            self.dbTable=env('dbTable')
            self.baseCurrency=env('baseCurrency')
            self.brokerFees=float(env('brokerFees'))
            self.liveTrading=env("liveTrading", 'False').lower() in ('true', '1', 't')
        except KeyError:
            print("No env variables set.")
            sys.exit(1)
        self.client = Client(apiKey, apiSecret, {'timeout':600})

    def closeTrade(self, resultData, i):
        stopId = resultData[resultData[0] == resultData[0].min()]
        if self.liveTrading == True:
            #get assets before sale
            symbolIsolated = re.sub(self.baseCurrency, '', self.bA[1][i])
            #wait a bit because otherwise api error
            time.sleep(1)
            assetsBefore = float(self.client.get_asset_balance(asset=self.baseCurrency)['free'])
            try:
                self.client.order_market_sell(symbol = self.bA[1][i], quantity = float(self.client.get_asset_balance(asset = symbolIsolated)['free']))
            except:
                print("Sell order was not executed on symbol: " + str(self.bA[1][i]))
                self.client.order_market_sell(symbol = self.bA[1][i], quantity = float(self.client.get_asset_balance(asset = symbolIsolated)['free'])*0.9)
            time.sleep(5)
            #get assets after sale
            assetsAfter = float(self.client.get_asset_balance(asset = self.baseCurrency)['free'])
            assetsResult = assetsAfter - assetsBefore
            percentChange = ((assetsResult / self.bA[5][i])*100)-100
        else: 
            percentChange = ((stopId[2] - self.bA[4][i]) / self.bA[4][i]) * 100 - self.brokerFees * 3.5
        #update database to include result
        sql = ("UPDATE " + self.dbTable + " SET" +
            " resultpercent = '" + str(float(percentChange)) +
            "', stopid = '" + str(float(stopId[0])) +
            "' WHERE id = '" + str(self.bA[0][i]) +
            "';")
        self.postgres.sqlUpdate(sql)

    def validate(self):
        self.postgres = postgresdbAccess.postgresAccess()
        sql = ("SELECT id, symbol, takeprofit, stoploss, askprice, positioncost" +
            " FROM " + self.dbTable + " WHERE" +
            " resultpercent IS NULL " +
            " AND takeprofit IS NOT NULL;")
        self.bA = pd.DataFrame(self.postgres.sqlQuery(sql))
        self.bA[0] = pd.to_numeric(self.bA[0])
        self.bA[2] = pd.to_numeric(self.bA[2])
        self.bA[3] = pd.to_numeric(self.bA[3])
        self.bA[4] = pd.to_numeric(self.bA[4])
        self.bA[5] = pd.to_numeric(self.bA[5])
        for i, row in self.bA.iterrows():
            sql = ("select id, askprice, bidprice from " + self.dbTable + " where id > '" + str(self.bA[0][i]) +
            "' and symbol = '" + str(self.bA[1][i]) + "';")
            validated = pd.DataFrame(self.postgres.sqlQuery(sql))
            if len(validated) > 0:
                validated = validated.apply(pd.to_numeric, errors='coerce')
                tpData = validated[validated[1] >= self.bA[2][i]]
                slData = validated[validated[1] <= self.bA[3][i]]
                if (len(slData) > 0 and len(tpData) > 0 and
                    slData[0].min() < tpData[0].min()):
                    self.closeTrade(slData, i)
                elif (len(slData) > 0 and len(tpData) > 0 and
                    slData[0].min() > tpData[0].min()):
                    self.closeTrade(tpData, i)
                elif len(slData) > 0:
                    self.closeTrade(slData, i)
                elif len(tpData) > 0:
                    self.closeTrade(tpData, i)
        self.postgres.databaseClose()
