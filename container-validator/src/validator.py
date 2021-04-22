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
    percentChange = ((float(stopId[1]) - float(bA[4][i])) / float(bA[4][i])) * 100
    #update database to include buy statement
    sql = ("UPDATE table001 SET" +
        " resultpercent = '" + str(percentChange) +
        "', stopid = '" + str(int(stopId[0])) +
        "' WHERE id = '" + str(bA[0][i]) +
        "';")
    print("updated db to include results")
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
        for i, row in bA.iterrows():
            #get point of sl and tp
            sql = ("select id, askprice from table001" + " where id > '" + str(int(bA[0][i])) + 
            "' and symbol = '" + str(bA[1][i]) + "';")
            validated = pd.DataFrame(timescale.sqlQuery(sql))
            tpData = validated[validated[1] >= float(bA[2][i])]
            slData = validated[validated[1] <= float(bA[3][i])]
            #check if sl data and tp data have been met
            if (len(slData) > 0 and len(slData) > 0 and
                slData[0].min() < tpData[0].min()):
                    print("executed 1")
                    calculateResult(slData, bA, i)
            elif (len(slData) > 0 and len(slData) > 0 and
                slData[0].min() > tpData[0].min()): 
                    print("executed 2")
                    calculateResult(tpData, bA, i)
            elif len(slData) > 0:
                print("executed 3")
                calculateResult(slData, bA, i)
            elif len(tpData) > 0:
                print("executed 4")
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
