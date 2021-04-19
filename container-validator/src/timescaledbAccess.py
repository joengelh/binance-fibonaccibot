import psycopg2
from psycopg2 import Error
import sys
import os
import itertools
from envs import env
from dotenv import load_dotenv

class timescaleAccess:
    def __init__(self):
        # import .env
        load_dotenv()
        #read env vars
        try:
            dbName=env("dbName")
            dbUser=env("dbUser")
            POSTGRES_PASSWORD=env("POSTGRES_PASSWORD")
            dbHost=env("dbHost")
            dbPort=env("dbPort")
        except KeyError:
            print("No env variables set.")
            sys.exit(1)
        #try connect to database
        try:
            # Connect to an existing database
            self.connection = psycopg2.connect(user=dbUser,
                                          password=POSTGRES_PASSWORD,
                                          host=dbHost,
                                          port=dbPort,
                                          database=dbName)
            #set connection to autocommit
            self.connection.rollback()
            self.connection.autocommit=True
            # Create a cursor to perform database operations
            self.cur = self.connection.cursor()
        except (Exception, Error) as error:
            print("Error while connecting to TimescaleDB", error)
            sys.exit(1)

    def dict2sql(self, dict4sql):
        self.columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dict4sql.keys())
        self.values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict4sql.values())
        self.types = ', '.join("'" for x in dict4sql.values())

    def tableCreate(self, writeDict, tableName = "table001"):
        self.dict2sql(writeDict)
        #create table if not exists
        dbHeader = "CREATE TABLE IF NOT EXISTS " + str(tableName) + " (\n"
        dbContent = ""
        for key, value in writeDict.items():
            if isinstance(value, bool):
                dbContent += str(key) + " BOOLEAN" + ",\n"
            elif isinstance(value, float):
                dbContent += str(key) + " DOUBLE PRECISION" + ",\n"
            elif isinstance(value, str):
                dbContent += str(key) + " TEXT" + ",\n"
            elif isinstance(value, int):
                dbContent += str(key) + " DOUBLE PRECISION" + ",\n"
        dbEnd = """time TIMESTAMPTZ NOT NULL,
id serial);"""
        try:
            self.cur.execute(dbHeader + dbContent + dbEnd)
        except:
            print("was not able to create table " + str(tableName) + " if not exists")
        
        #make hypertable from table
        sql = "SELECT create_hypertable('" + str(tableName) + "','time');"
        try:
            self.cur.execute(sql)
        except:
            print("table " + str(tableName) + " is already hypertable")

    def insertColumn(self, name, tableName = "table001"):
        sql = "ALTER TABLE " + str(tableName) + " ADD COLUMN IF NOT ExISTS " + str(name) + " DOUBLE PRECISION;"
        try: 
            self.cur.execute(sql)
        except:
            print("column " + str(name) + " already exists")
    
    def sqlUpdate(self, sql):
        try:
            self.cur.execute(sql)
        except:
            print("error in update")

    def sqlQuery(self, sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
        except:
            print("error in query")
        
        return result

    def insertRow(self, writeDict, tableName = "table001"):
        self.dict2sql(writeDict)
        #append dict as row to table
        sql = "INSERT INTO %s ( %s, time) VALUES ( %s, NOW() );" % (str(tableName), self.columns, self.values)
        #shitty solution to a shitty problem, API returns `symbol` instead of 'symbol'
        sql = sql.replace("`", "")
        try:
            self.cur.execute(sql)
        except (Exception, psycopg2.Error)as error:
            print(error.pgerror)
        
    def databaseClose(self):
        self.cur.close()
        self.connection.close()
