import time
import config
import os
import redis
import pickle

r=redis.Redis(host="127.0.0.1",port=6379)

time.sleep(5)


start_time=pickle.loads(r.get("start_time"))
run_time=config.run_time



def timer(start_time,run_time):
    end_time=time.time()
    print(int(end_time-start_time)," diff")
    if run_time <= int(end_time-start_time):
        os.system("mn -c")
        os.system("killall python")

while True:
    time.sleep(1)
    timer(start_time,run_time)