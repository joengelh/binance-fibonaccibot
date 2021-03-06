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
import redis


#import classes from ./ folder
import postgresdbAccess

class predictAccess:
    def __init__(self):
        try:
            self.dbTable=env("dbTable")
            self.baseCurrency=env("baseCurrency")
            self.liveTrading=env("liveTrading", 'False').lower() in ('true', '1', 't')
            self.brokerFees=float(env('brokerFees'))
            self.liveVolume=float(env('liveVolume'))
            self.POSTGRES_PASSWORD=env('POSTGRES_PASSWORD')
            self.dbHost=env('dbHost')
        except KeyError:
            print("No env variables set.")
            sys.exit(1)

    def reset(self, r):
        r.setex(
            "simulatedAvg",
            timedelta(minutes=15),
            value="NaN %"
        )
        if self.liveTrading:    
            r.setex(
                "simulatedSum",
                timedelta(minutes=15),
                value="NaN " + self.baseCurrency
            )
        else:
            r.setex(
                "simulatedSum",
                timedelta(minutes=15),
                value="NaN %"
            )
        r.setex(
            "simulatedWinner",
            timedelta(minutes=15),
            value="NaN"
        )  
        r.setex(
            "simulatedLoser",
            timedelta(minutes=15),
            value="NaN"
        )

    def simulate(self):
        #initiate db connection
        postgres = postgresdbAccess.postgresAccess()
        r = redis.Redis(host=self.dbHost, 
            port=6379, 
            db=0, 
            password=self.POSTGRES_PASSWORD)
        #get unique simbol list
        sql = ("SELECT symbol, askprice FROM " + self.dbTable + 
            " where resultpercent is null and takeprofit is not null;")
        openTrades = pd.DataFrame(postgres.sqlQuery(sql))
        if len(openTrades) > 0:
            if self.liveTrading:
                result = []
                sql = ("SELECT symbol, askprice, positioncost FROM " + self.dbTable + 
                    " where resultpercent is null and positioncost is not null;")
                openTrades = pd.DataFrame(postgres.sqlQuery(sql))
                if len(openTrades) > 0:
                    for index, row in openTrades.iterrows():
                        #query for simulated stopid
                        sql = ("SELECT bidprice" +
                            " FROM " + self.dbTable + " WHERE" +
                            " symbol = '" + row[0] +
                            "' ORDER BY id DESC LIMIT 1;")
                        stopId = pd.DataFrame(postgres.sqlQuery(sql))
                        result.append((((float(stopId[0][0]) - float(row[1])) / float(row[1])) 
                            * 100 - self.brokerFees * 2) / 100 * float(row[2]))
                    r.setex(
                    "simulatedAvg",
                    timedelta(minutes=15),
                    value=str(round(sum(result)/len(result), 2)) + " %"
                    )
                    r.setex(
                        "simulatedSum",
                        timedelta(minutes=15),
                        value=str(round(sum(result), 2)) + " " + self.baseCurrency
                    )
                    r.setex(
                        "simulatedWinner",
                        timedelta(minutes=15),
                        value=round(sum(i > 0 for i in result), 2)
                    )  
                    r.setex(
                        "simulatedLoser",
                        timedelta(minutes=15),
                        value=round(sum(i < 0 for i in result), 2)
                    )

            else:
                resultPercent = []
                for index, row in openTrades.iterrows():
                    #query for simulated stopid
                    sql = ("SELECT bidprice" +
                        " FROM " + self.dbTable + " WHERE" +
                        " symbol = '" + row[0] +
                        "' ORDER BY id DESC LIMIT 1;")
                    stopId = pd.DataFrame(postgres.sqlQuery(sql))
                    resultPercent.append(((float(stopId[0][0]) - float(row[1])) / float(row[1])) * 100 - self.brokerFees * 2)
                r.setex(
                    "simulatedAvg",
                    timedelta(minutes=15),
                    value=str(round(sum(resultPercent)/len(resultPercent), 2)) + " %"
                )
                r.setex(
                    "simulatedSum",
                    timedelta(minutes=15),
                    value=str(round(sum(resultPercent), 2)) + " %"
                )
                r.setex(
                    "simulatedWinner",
                    timedelta(minutes=15),
                    value=round(sum(i > 0 for i in resultPercent), 2)
                )  
                r.setex(
                    "simulatedLoser",
                    timedelta(minutes=15),
                    value=round(sum(i < 0 for i in resultPercent), 2)
                )
        else:
            self.reset(r)
        postgres.databaseClose()
