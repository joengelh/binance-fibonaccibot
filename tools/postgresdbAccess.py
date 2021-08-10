import psycopg2
from psycopg2 import Error
import sys
import os
import itertools
from envs import env

class postgresAccess:
    def __init__(self):
        #read env vars
        try:
            dbName=env("dbName")
            dbUser=env("dbUser")
            POSTGRES_PASSWORD=env("POSTGRES_PASSWORD")
            dbHost=env("dbHost")
            dbPort=env("dbPort")
            self.dbTable=env("dbTable")
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
            print("Error while connecting to Postgres", error)
            sys.exit(1)

    def dict2sql(self, dict4sql):
        self.columns = ', '.join(str(x).replace('/', '_') for x in dict4sql.keys())
        self.values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict4sql.values())

    def tableCreate(self, writeDict):
        #create table if not exists
        dbHeader = "CREATE TABLE IF NOT EXISTS " + self.dbTable + " (\n"
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
        dbEnd = "time TIMESTAMPTZ NOT NULL, id serial);"
        try:
            self.cur.execute(dbHeader + dbContent + dbEnd)
        except:
            print("was not able to create table " + self.dbTable + " if not exists")
        
        #make hypertable from table
        sql = "SELECT create_hypertable('" + self.dbTable + "','time');"
        try:
            self.cur.execute(sql)
        except:
            print("table " + self.dbTable + " is already hypertable")

    def insertColumns(self, WriteCol):
        dbHeader = "ALTER TABLE " + self.dbTable + " (\n"
        dbContent = ""
        for key, value in writeCol.items():
            if isinstance(value, bool):
                dbContent += "ADD COLUMN IF NOT EXISTS" + str(key) + " BOOLEAN" + ",\n"
            elif isinstance(value, float):
                dbContent += "ADD COLUMN IF NOT EXISTS" + str(key) + " DOUBLE PRECISION" + ",\n"
            elif isinstance(value, str):
                dbContent += "ADD COLUMN IF NOT EXISTS" + str(key) + " TEXT" + ",\n"
            elif isinstance(value, int):
                dbContent += "ADD COLUMN IF NOT EXISTS" + str(key) + " DOUBLE PRECISION" + ",\n"
        dbEnd = "time TIMESTAMPTZ NOT NULL, id serial);"
        try:
            self.cur.execute(dbHeader + dbContent + dbEnd)
        except:
            print("was not able to add column " + self.dbTable + " if not exists")
    
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

    def insertRow(self, writeDict):
        self.dict2sql(writeDict)
        #append dict as row to table
        sql = "INSERT INTO %s ( %s, time) VALUES ( %s, NOW() );" % (self.dbTable, self.columns, self.values)
        try:
            self.cur.execute(sql)
        except (Exception, psycopg2.Error)as error:
            print(error.pgerror)
        
    def databaseClose(self):
        self.cur.close()
        self.connection.close()
