#import modules
import json
from binance.client import Client
import pandas as pd
import os
from envs import env

#import classes from ./ folder
import timescaledbAccess

class tradingAccess:
    def __init__(self):
        #read fibonacci retracements  from json
        with open('fibLvl.json') as file:
            self.fibLvl = json.load(file)
        #read if live trading is enabled
        try:
            self.liveTrading=env("liveTrading", 'False').lower() in ('true', '1', 't')
            self.liveVolume=env("liveVolume")
            apiSecret=env('apiSecret')
            apiKey=env('apiKey')
        except KeyError:
            print("No env variables set.")
            sys.exit(1)
        #connect to binance to get current balance
        self.client = Client(apiKey, apiSecret, {'timeout':600})

    def ocoOrder(self, tick, sl, tp):
        orderString = ("python3 ./execute_orders.py" +
                " --symbol " + str(tick['symbol']) +
                " --buy_type market" +
                " --total " + str(self.liveVolume) +
                " --profit " + str((tp / float(tick['askPrice']) - 1) * 100) +
                " --loss " + str((sl / float(tick['askPrice']) - 1) * -100))
        print("===================================")
        os.system(orderString)

    def writeAdvice(self, fib, i, large, cor):
        sql = ("UPDATE table001 SET " +
                            " takeProfit = '" + str(fib[2][i+2]) +
                            "', stopLoss = '" + str(fib[2][i-1]) +
                            "', corValue = '" + str(cor) +
                            "', startId = '" + str(large[0].min()) +
                            "', midId = '" + str(large[0].max()) +
                            "', fibLevel = '" + str(fib[0][i]) +
                            "', managedAssets = '" + str(self.client.get_asset_balance(asset='BNB')['free']) +
                            "' WHERE id IN(SELECT max(id) FROM table001);")
        self.timescale.sqlUpdate(sql)

    def runCalculation(self, tick):
        self.timescale = timescaledbAccess.timescaleAccess()
        sql = ("SELECT id, askprice FROM table001 WHERE symbol LIKE '" + tick['symbol'] + 
            "' AND time > NOW() - INTERVAL '12 hours" + 
            "' AND time < NOW() - INTERVAL '2 hours';")
        largeData = pd.DataFrame(self.timescale.sqlQuery(sql))
        if len(largeData) >= 1:    
            #convert columns id and askprice to float
            largeData = largeData.apply(pd.to_numeric, errors='coerce')
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
            sql = "SELECT count(*) FROM table001 WHERE takeprofit is not null and resultpercent is null;"
            #get current correlation of price and id
            corValue = largeData[0].corr(largeData[1])
            # open trade and write advice if no trade is open yet
            for i in range(1,3):
                if ((int(self.timescale.sqlQuery(sql)[0][0]) == 0 or self.liveTrading == False) and
                    float(tick['askPrice']) > fibRetracement[2][i] and
                    float(tick['askPrice']) < fibRetracement[3][i]):
                        if self.liveTrading == True:
                            self.ocoOrder(tick, fibRetracement[2][i-1], fibRetracement[2][i+2])
                        self.writeAdvice(fibRetracement, i, largeData, corValue)
        self.timescale.databaseClose()
