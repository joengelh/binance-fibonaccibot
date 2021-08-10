#import modules
from dotenv import load_dotenv
from envs import env
import time
import re
import os
import datetime
from datetime import timedelta
import redis
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

apiId="7095481"
phoneNumber="+4915752313100"
apiHash="c94cfb9396cd0d6c196bcad462eed3f0"
token="1910855017:AAHmaUox-ggaloZpQnIdR256l47REb6zDi"

r = redis.Redis(host="192.168.2.8", 
    port=6379, 
    db=0, 
    password="password")
        
message = ("openTrades: " + r.get("openTrades").decode('utf-8') + "\n" +
    "simulatedSum: " + r.get("simulatedSum").decode('utf-8') + "\n" +
     "sumResult: " + r.get("sumResult").decode('utf-8'))

client = TelegramClient('session', apiId, apiHash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phoneNumber)
    client.sign_in(phoneNumber, input('Enter the code: ')) 

print(client.get_me().stringify())

receiver = InputPeerUser(176741944, 903919511858501423)
message="hello"
client.send_message(receiver, message, parse_mode='html')

client.disconnect()
