import redis
import pickle
from config import *
import time
import migration


r=redis.Redis(host="127.0.0.1",port=6379)

unload_time = 10


while True:

    ctrls=pickle.loads(r.get("controllers"))
    swths=pickle.loads(r.get("switches"))
    thresh=pickle.loads(r.get("threshold"))
    ctrls_db={}
    
    

    for i in range(len(controllers)):
        ctrls_db["c"+str(i+1)]=pickle.loads(r.get("c"+str(i+1)))

    for controller in ctrls.values():
        
        for switch in ctrls_db[controller['name']]['switches'].values():
            switch_name=switch['name']
            packet_in_count=switch['packet_in_count']
            if packet_in_count>=thresh:
                switch['packet_in_count']=0
                temp_ctrl=ctrls_db[controller['name']]
                r.set(temp_ctrl['name'],pickle.dumps(temp_ctrl))
                
                # print(ctrls_db)

                print("Switch "+switch_name+" from controller "+controller['name']+" has packet count set to 0")
        # print("---------------------------------------------------------------------")
    

    time.sleep(unload_time)

        
