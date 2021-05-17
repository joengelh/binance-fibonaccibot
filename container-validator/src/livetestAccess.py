#import modules
import json
from binance.client import Client
import pandas as pd
from envs import env

#import classes from ./ folder
import timescaledbAccess

class liveAccess:
    def __init__(self):
        self.timescale = timescaledbAccess.timescaleAccess()
        try:
            self.liveVolume=env("liveVolume")
            apiSecret=env('apiSecret')
            apiKey=env('apiKey')
        except KeyError:
            print("No env variables set.")
            sys.exit(1)
        #connect to binance to get current balance
        self.client = Client(apiKey, apiSecret, {'timeout':600})

    def validate(self):
        sql = ("SELECT id, askprice" +
            " FROM table001 WHERE" +
            " resultpercent IS NULL " +
            " AND takeprofit IS NOT NULL;")
        bA = pd.DataFrame(self.timescale.sqlQuery(sql))
        bA = bA.apply(pd.to_numeric, errors='coerce')
        #check if trade has been closed
        if (len(bA) > 0 and
            len(self.client.get_open_orders() == 0)):
                percentChange = (self.client.get_asset_balance(asset='BNB')['free'] - bA[managedassets]) / self.liveVolume
                #get max id
                sql = ("select symbol from table001 where id = '" + str(bA[0]) + "';")
                symbol = pd.DataFrame(timescale.sqlQuery(sql))
                sql = ("select max(id) from table001 where symbol = '" + str(symbol[0][0]) + "';")
                maxId = pd.DataFrame(timescale.sqlQuery(sql))
                sql = ("UPDATE table001 SET" +
                " resultpercent = '" + str(percentChange) +
                "', stopid = max(id)" +
                " WHERE id = '" + str(maxId[0][0]) +
                "';")
                timescale.sqlUpdate(sql)
                timescale.databaseClose()
        else: pass
            
        
