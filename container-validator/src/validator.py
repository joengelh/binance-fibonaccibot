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

def runValidation():
    timescale = timescaledbAccess.timescaleAccess()
    sql = ("SELECT id, symbol, takeprofit, stoploss, askprice" +
          " FROM table001 WHERE" + 
          " resultpercent IS NULL " +
          " AND takeprofit IS NOT NULL;")
    bA = pd.DataFrame(timescale.sqlQuery(sql))
    if len(bA) > 0:
        for i, row in bA.iterrows():
            #get point of sl and tp
            sql = ("select id, askprice from table001" +
                " where (id > '" + str(bA[0][i]) + "' and symbol = '" + str(bA[1][i]) + 
                "') and (askprice < '" + str(bA[3][i]) + "' or askprice > '" + str(bA[2][i]) +
                "');")
            validated = pd.DataFrame(timescale.sqlQuery(sql))
            if len(validated) > 0:
                #calculate result
                stopId = validated[validated[0] == validated[0].max()]
                percentChange = ((float(stopId[1]) - float(bA[4][i])) / float(bA[4][i])) * 100 
                #update database to include buy statement
                sql = ("UPDATE table001 SET" +
                " resultpercent = '" + str(percentChange) +
                "' WHERE id = '" + str(bA[0][i]) +
                "';")
                timescale.sqlUpdate(sql)
    timescale.databaseClose()

#check if result has been reached every minute
schedule.every().minute.at(":30").do(runValidation)

#repeat
while True:
    schedule.run_pending()
    time.sleep(1)
