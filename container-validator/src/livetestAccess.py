#import modules
import json
import pandas as pd
import schedule
import time

#import classes from ./ folder
import timescaledbAccess

class liveAccess:
    def __init__(self):
        self.timescale = timescaledbAccess.timescaleAccess()
        try:
            self.liveVolume=env("liveVolume")
        except KeyError:
            print("No env variables set.")
            sys.exit(1)

def calculateResult(resultData, bA, i):
    stopId = resultData[resultData[0] == resultData[0].min()]
    percentChange = ((stopId[1] - bA[4][i]) / bA[4][i]) * 100
    sql = ("UPDATE table001 SET" +
        " resultpercent = '" + str(float(percentChange)) +
        "', stopid = '" + str(float(stopId[0])) +
        "' WHERE id = '" + str(bA[0][i]) +
        "';")
    timescale.sqlUpdate(sql)

def validate():
    sql = ("SELECT id, askprice" +
        " FROM table001 WHERE" +
        " resultpercent IS NULL " +
        " AND takeprofit IS NOT NULL;")
    bA = pd.DataFrame(self.timescale.sqlQuery(sql))
    bA = bA.apply(pd.to_numeric, errors='coerce')
    if (len(bA) > 0 and
        timescale):
        for i, row in bA.iterrows():
            
    timescale.databaseClose()