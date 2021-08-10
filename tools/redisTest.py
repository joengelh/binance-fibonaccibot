#import modules
import redis

r = redis.Redis(host="192.168.2.8", port=6379, db=0, password="password")
r.set("openTrades", "4")
r.set("simulatedSum", "0.12")
r.set("sumResult", "0.01")
hello = "yeye" + r.get('openTrades').decode('utf-8')
print(hello)
