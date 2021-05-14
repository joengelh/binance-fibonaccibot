#import modules
import json
import pandas as pd
import os
from dotenv import load_dotenv
from envs import env


with open('fibLvl.json') as file:
    fibLvl = json.load(file)
fibRetracement = pd.DataFrame(fibLvl)

print(fibRetracement[2][1])