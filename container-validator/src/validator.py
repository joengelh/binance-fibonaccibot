#import modules
import json
import pandas as pd
import schedule
import time

#import classes from ./ folder
import timescaledbAccess

#read fibonacci retracements  from json
with open('fibLvl.json') as file:
    fibLvl = json.load(file)

def calculateResult(resultData, bA, i):
    stopId = resultData[resultData[0] == resultData[0].min()]
    percentChange = ((stopId[1] - bA[4][i]) / bA[4][i]) * 100
    #update database to include buy statement
    sql = ("UPDATE table001 SET" +
        " resultpercent = '" + str(float(percentChange)) +
        "', stopid = '" + str(float(stopId[0])) +
        "' WHERE id = '" + str(bA[0][i]) +
        "';")
    timescale.sqlUpdate(sql)

def runValidation():
    global timescale
    timescale = timescaledbAccess.timescaleAccess()
    sql = ("SELECT id, symbol, takeprofit, stoploss, askprice" +
        " FROM table001 WHERE" +
        " resultpercent IS NULL " +
        " AND takeprofit IS NOT NULL;")
    bA = pd.DataFrame(timescale.sqlQuery(sql))
    if len(bA) > 0:
        bA[0] = pd.to_numeric(bA[0])
        bA[2] = pd.to_numeric(bA[2])
        bA[3] = pd.to_numeric(bA[3])
        bA[4] = pd.to_numeric(bA[4])
        for i, row in bA.iterrows():
            sql = ("select id, askprice from table001" + " where id > '" + str(bA[0][i]) +
                    "' and symbol = '" + str(bA[1][i]) + "';")
            validated = pd.DataFrame(timescale.sqlQuery(sql))
            if len(validated) > 0:
                validated[0] = pd.to_numeric(validated[0])
                validated[1] = pd.to_numeric(validated[1])
                tpData = validated[validated[1] >= bA[2][i]]
                slData = validated[validated[1] <= bA[3][i]]
                if (len(slData) > 0 and len(slData) > 0 and
                    slData[0].min() < tpData[0].min()):
                    calculateResult(slData, bA, i)
                elif (len(slData) > 0 and len(slData) > 0 and
                    slData[0].min() > tpData[0].min()):
                    calculateResult(tpData, bA, i)
                elif len(slData) > 0:
                    calculateResult(slData, bA, i)
                elif len(tpData) > 0:
                    calculateResult(tpData, bA, i)
                else:
                    print("waiting for more data")
    timescale.databaseClose()

#check if result has been reached every minute
schedule.every().minute.at(":30").do(runValidation)

#repeat
while True:
    schedule.run_pending()
    time.sleep(1)
