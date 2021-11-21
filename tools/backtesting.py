#import modules
import json
import pandas as pd
from dotenv import load_dotenv
from envs import env
import time
import re
import os
import datetime
from datetime import timedelta
import statistics
import numpy as np
from scipy.stats import kurtosis, skew

#import classes from ./ folder
import postgresdbAccess

#read fibonacci retracements  from json
with open('fibLvl.json') as file:
    fibLvl = json.load(file)

def writeTrade(openPositions, row, postgres):
    openPositions['resultPercent'] = (((row[4] - 
        openPositions['askPrice']) / openPositions['askPrice']) * 
        100 - brokerFees * 2.55)
    openPositions['stopId'] = row[0]        
    closeSql = ("UPDATE " + dbTable + " SET" +
        " startId = '" + str(int(openPositions['startId'])) +
        "', fibLevel = '" + str(openPositions['fibLevel']) +
        "', midId = '" + str(int(openPositions['midId'])) +
        "', corValue = '" + str(openPositions['corValue']) +
        "', takeProfit = '" + str(openPositions['takeProfit']) +
        "', stopLoss = '" + str(openPositions['stopLoss']) +  
        "', resultpercent = '" + str(openPositions['resultPercent']) +
        "', stopid = '" + str(openPositions['stopId']) +
        "', skew = '" + str(openPositions['skew']) +
        "', stdev = '" + str(openPositions['stDev']) +
        "', kurtosis = '" + str(openPositions['kurtosis']) +
        "' WHERE id = '" + str(int(openPositions['id'])) +
        "';")
    postgres.sqlUpdate(closeSql)

def backtest():
    #initiate empty open positions
    openPositions = {}
    #initiate postgresdb class
    postgres = postgresdbAccess.postgresAccess()
    #get unique simbol list
    sql = ("SELECT distinct symbol FROM " + dbTable + ";")
    uniqueSymbol = pd.DataFrame(postgres.sqlQuery(sql))
    uniqueSymbol = uniqueSymbol[0]
    #initiate empty percent bar
    percentBar = 0
    #loop over every symbol in symbol list
    for symbol in uniqueSymbol:
        #print progress
        print(percentBar, " / ", len(uniqueSymbol))
        percentBar = percentBar + 1
        #skip if symbol is not to be considered
        #null askprice is sorted out with crawler already
        if not (symbol.endswith(baseCurrency) and
               len(symbol) < 11):
            continue
        #check if open position was left over from last symbol and simulate close
        if openPositions:
            writeTrade(openPositions, row, postgres)
            openPositions = {}
        #query for every line for symbol
        sql = ("SELECT id, time, symbol, askprice, " +
               "bidprice, highprice, quotevolume, " +
               "pricechangepercent, weightedavgprice, openprice" +
            " FROM " + dbTable + " WHERE" +
            " symbol like '" + symbol + "' order by id;")
        print(sql)
        bigData = pd.DataFrame(postgres.sqlQuery(sql))
        bigData[0] = pd.to_numeric(bigData[0], errors='coerce', downcast='float')
        bigData[1] = pd.to_datetime(bigData[1])
        bigData[3] = pd.to_numeric(bigData[3], errors='coerce', downcast='float')
        bigData[4] = pd.to_numeric(bigData[4], errors='coerce', downcast='float')
        bigData[6] = pd.to_numeric(bigData[6], errors='coerce', downcast='float')
        bigData[7] = pd.to_numeric(bigData[7], errors='coerce', downcast='float')
        bigData[8] = pd.to_numeric(bigData[8], errors='coerce', downcast='float')
        bigData[9] = pd.to_numeric(bigData[9], errors='coerce', downcast='float')
        #get start of timedelta
        bigData[5] = bigData[1] - timedelta(hours=33)
        #loop over every row
        for index, row in bigData.iterrows():
            before_start_date = bigData[1] <= row[5]
            if len(bigData.loc[before_start_date]) > 0:
                #get data for consideration
                after_start_date = bigData[1] >= row[5]
                before_end_date = bigData[1] <= row[1]
                between_two_dates = after_start_date & before_end_date
                fibDates = bigData.loc[between_two_dates]
                diff = fibDates[3].max() - fibDates[3].min()
                # calculate fibRetracements
                fibRetracement = pd.DataFrame(fibLvl)
                maxAsk = fibDates[3].max()
                for lvl in fibRetracement:
                    fibRetracement[1] =  maxAsk - diff * fibRetracement[0]
                    fibRetracement[2] = fibRetracement[1] * 0.999
                    fibRetracement[3] = fibRetracement[1] * 1.001
               
                #calculate corvalue
                corValue = fibDates[0].corr(fibDates[3])

                #get statistical parameters
                statisticsTools = {}
                statisticsTools["stDev"] = statistics.stdev(fibDates[3])
                statisticsTools["skew"] = skew(fibDates[3])
                statisticsTools["kurtosis"] = kurtosis(fibDates[3])
                
                #if an open position exists, check if it can be closed
                if openPositions:
                    if (row[3] <= openPositions['stopLoss'] or
                        row[3] >= openPositions['takeProfit']):
                            writeTrade(openPositions, row, postgres)
                            #clear open position
                            openPositions = {}
                else:
                    #loop over considered fibonacciretracements
                    for i in [7]:
                        #check if buy requirements are met
                        if (row[7] >= 0 or
                            row[7] <= -10):
                            if (statisticsTools["skew"] <= -0.1 and
                                row[3] >= fibRetracement[2][i] and
                                row[3] <= fibRetracement[3][i]):
                                    openPositions['startId'] = fibDates[0].min()
                                    openPositions['id'] = row[0]
                                    openPositions['midId'] = fibDates[0].max()
                                    openPositions['bidPrice'] = row[4]
                                    openPositions['fibLevel'] = i
                                    openPositions['symbol'] = symbol
                                    openPositions['askPrice'] = row[3]
                                    openPositions['corValue'] = corValue
                                    openPositions['stDev'] = statisticsTools["stDev"]
                                    openPositions['skew'] = statisticsTools["skew"]
                                    openPositions['kurtosis'] = statisticsTools["kurtosis"]
                                    openPositions['takeProfit'] = fibRetracement[2][i+5]
                                    openPositions['stopLoss'] = fibRetracement[2][i-1]
    #close database connection
    postgres.databaseClose()

load_dotenv('../.env')
try:
    dbTable="backtesting"
    baseCurrency=env('baseCurrency')
    brokerFees=float(env('brokerFees'))
except KeyError:
    print("No env variables set.")
    sys.exit(1)
backtest()
