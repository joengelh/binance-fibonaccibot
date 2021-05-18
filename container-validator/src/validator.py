#import modules
import schedule
import time
from envs import env

#import own classes
import backtestAccess
import livetestAccess

def validator():
    try:
        liveTrading=env("liveTrading", 'False').lower() in ('true', '1', 't')
    except KeyError:
        print("No env variables set.")
        sys.exit(1)
    if liveTrading == True:
        liveTest = livetestAccess.liveAccess()
        liveTest.validate()
    else:
        backTest = backtestAccess.backAccess()
        backTest.validate()

schedule.every().minute.at(":45").do(validator)

while True:
    schedule.run_pending()
    time.sleep(1)
