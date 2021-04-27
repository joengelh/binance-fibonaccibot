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

    def ocoOrder(self, symbol, price, slp, tpp):
        orderString = ("python3 ./execute_orders.py" +
                " --symbol " + symbol +
                " --buy_type market" +
                " --total 1" +
                " --profit " + str(tpp) +
                " --loss " + str(slp) +
                " &>/dev/null &")
        print("===================================")
        print(orderString)
        os.system(orderString)

    def writeAdvice(self, fib, large, i):
        sql = ("UPDATE table001 SET " +
                            " takeProfit = '" + str(fib[2][i+2]) +
                            "', stopLoss = '" + str(fib[2][i-1]) +
                            "', corValue = '" + str(large[10].corr(large[1])) +
                            "', startId = '" + str(large[10].min()) +
                            "', fibLevel = '" + str(fib[0][i]) +
                            "' WHERE id = '" + str(large[10].max()) +
                            "';")
        self.timescale.sqlUpdate(sql)

    def runCalculation(self, tick):
        self.timescale = timescaledbAccess.timescaleAccess()
        sql = ("SELECT * FROM table001 WHERE symbol LIKE '" + tick['symbol'] + 
            "' AND time > NOW() - INTERVAL '10 hours';")
        largeData = pd.DataFrame(self.timescale.sqlQuery(sql))
        #convert columns id and askprice to float
        largeData[10] = largeData[10].apply(pd.to_numeric, downcast='float', errors='coerce')
        largeData[1] = largeData[1].apply(pd.to_numeric, downcast='float', errors='coerce')
        #calculate diff
        diff = largeData[1].max() - largeData[1].min()
        # calculate fibRetracements
        fibRetracement = pd.DataFrame(self.fibLvl)
        maxAsk = largeData[1].max()
        for lvl in fibRetracement:
            fibRetracement[1] =  maxAsk - diff * fibRetracement[0]
            fibRetracement[2] = fibRetracement[1] * 0.9995
            fibRetracement[3] = fibRetracement[1] * 1.0005
        #check if there is a reason to buy
        loopRange = range(1, len(fibRetracement) -2)
        for i in loopRange:
            if (float(tick['askPrice']) > fibRetracement[2][i] and
            float(tick['askPrice']) < fibRetracement[3][i]):
                #check if there is still an open trade
                sql = ("SELECT count(*) FROM table001 WHERE takeprofit is not null" +
                      " and resultpercent is null;")
                #check if this isnt the atl in the past 9 + 1 hours
                sql2 = ("SELECT count(*) FROM table001 WHERE symbol LIKE '" +
                        tick['symbol'] + "' AND time > NOW() - INTERVAL '10 hours'" +
                        " AND time < NOW() - INTERVAL '1 hour'" +
                        " AND askprice <= '" + str(tick['askPrice']) + "';")
                if (self.timescale.sqlQuery(sql)[0][0] < 1 and
                        self.timescale.sqlQuery(sql2)[0][0] > 0 and
                        fibRetracement[0][i] >= 1):
                    self.writeAdvice(fibRetracement, largeData, i)                        
                    #calculate positive percentage in 0-100% for sl and tp
                    takeProfitPercent = (fibRetracement[2][i+2] / float(tick['askPrice']) -1) * 100
                    stopLossPercent = (fibRetracement[2][i-1] / float(tick['askPrice']) - 1) * -100
                    self.ocoOrder(tick['symbol'], stopLossPercent, takeProfitPercent)

        self.timescale.databaseClose()

