#import modules
import json
import sys
import os
import itertools
from dotenv import load_dotenv
import schedule
import time
from envs import env
 
#import classes from ./ folder
import predictionAccess

def update():
    #initiate own classes
    oracle = predictionAccess.predictAccess()
    oracle.simulate()

#write prediction every minute
schedule.every().minute.at(":40").do(update)

#repeat
while True:
    schedule.run_pending()
    time.sleep(1)
