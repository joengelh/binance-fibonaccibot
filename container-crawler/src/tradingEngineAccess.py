#import modules
import json
import pandas as pd
import os

#import classes from ./ folder
import timescaledbAccess

class tradingAccess:
    def __init__(self):
        #read fibonacci retracements  from json
        with open('fibLvl.json') as file:
            self.fibLvl = json.load(file)
        with open('tradableLvl.json') as file:
            self.tradableLvl = json.load(file)

    def ocoOrder(self, symbol, slp, tpp):
        orderString = ("python3 ./execute_orders.py" +
                " --symbol " + symbol +
                " --buy_type market" +
                " --total 0.1" +
                " --profit " + str(tpp) +
                " --loss " + str(slp) +
                " &>/dev/null &")
        print("===================================")
        print(orderString)
        #os.system(orderString)

    def writeAdvice(self, fib, large, i):
        sql = ("UPDATE table001 SET " +
                            " takeProfit = '" + str(fib[2][i+2]) +
                            "', stopLoss = '" + str(fib[2][i-1]) +
                            "', corValue = '" + str(large[22].corr(large[9])) +
                            "', startId = '" + str(large[22].min()) +
                            "', fibLevel = '" + str(fib[0][i]) +
                            "' WHERE id = '" + str(large[22].max()) +
                            "';")
        self.timescale.sqlUpdate(sql)

    def runCalculation(self, tick):
        self.timescale = timescaledbAccess.timescaleAccess()
        sql = ("SELECT * FROM table001 WHERE symbol LIKE '" + tick['symbol'] + 
            "' AND time > NOW() - INTERVAL '10 hours';")
        largeData = pd.DataFrame(self.timescale.sqlQuery(sql))
        #convert columns id and askprice to float
        largeData[22] = largeData[22].apply(pd.to_numeric, downcast='float', errors='coerce')
        largeData[9] = largeData[9].apply(pd.to_numeric, downcast='float', errors='coerce')
        #calculate diff
        diff = largeData[9].max() - largeData[9].min()
        if float(tick['askPrice']) < ((float(tick['highPrice']) - diff * 0.1)):
            # calculate fibRetracements
            fibRetracement = pd.DataFrame(self.fibLvl)
            maxAsk = largeData[9].max()
            for lvl in fibRetracement:
                fibRetracement[1] =  maxAsk - diff * fibRetracement[0]
                fibRetracement[2] = fibRetracement[1] * 0.9995
                fibRetracement[3] = fibRetracement[1] * 1.0005
            #check if there is a reason to buy
            loopRange = range(1, len(fibRetracement) -2)
            for i in loopRange:
                if (float(tick['askPrice']) > fibRetracement[2][i] and
                float(tick['askPrice']) < fibRetracement[3][i]):
                    #check if advice has been given in the last 10 minutes for the pair
                    sql = ("SELECT count(*) FROM table001 WHERE symbol LIKE '" + 
                            tick['symbol'] + "' AND time > NOW() - INTERVAL '15 minutes'" +
                            " AND takeprofit is not null;")
                    if self.timescale.sqlQuery(sql)[0][0] < 1:
                        self.writeAdvice(fibRetracement, largeData, i)                        
                        if fibRetracement[0][i] in self.tradableLvl:
                            #calculate positive percentage in 0-100% for sl and tp
                            takeProfitPercent = (fibRetracement[2][i+2] / float(tick['askPrice']) -1) * 100
                            stopLossPercent = (fibRetracement[2][i-1] / float(tick['askPrice']) - 1) * -100
                            self.ocoOrder(tick['symbol'], stopLossPercent, takeProfitPercent)
        
        self.timescale.databaseClose()

