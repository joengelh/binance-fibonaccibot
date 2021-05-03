#import modules
from binance.client import Client
from dotenv import load_dotenv
from envs import env

#define start balance
startBalance=5.3591291

#import classes from ./ folder
import timescaledbAccess

#read env vars
load_dotenv()

try:                                                                                       
    apiSecret=env('apiSecret')
    apiKey=env('apiKey')
except KeyError:
    print("No env variables set.")
    sys.exit(1)

#timescale = timescaledbAccess.timescaleAccess()
client = Client(apiKey, apiSecret, {'timeout':600})
tickers = client.get_ticker()

balance = float(client.get_asset_balance(asset='BNB')['free'])

print(str(round((((balance/startBalance) * 100) - 100),2)) + "%")