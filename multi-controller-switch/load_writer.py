import redis
import pickle
import config
import algorithm
import os
import time

r=redis.Redis(host='127.0.0.1',port=6379)

interval=5
count=interval
runtime=config.run_time
controllers=pickle.loads(r.get("controllers"))





try:
    os.system("rm *_load_data.txt")
except:
    pass

# print(algorithm.total_packet_in_count(ctrls[0]))
while(count<=runtime):
    time.sleep(interval)
    ctrls=[]
    for i in controllers.values():
        ctrls.append(pickle.loads(r.get(i['name'])))
    for i in ctrls:
        
        f=open(i['name']+"_load_data.txt","a")
        load=algorithm.total_packet_in_count(i)
        f.write(i['name']+" "+str(load)+" "+str(count)+"\n")
        f.close()
    count+=interval