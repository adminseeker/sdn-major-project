import redis
import pickle
from config import *
import time



r=redis.Redis(host="127.0.0.1",port=6379)

pickled_controllers=pickle.dumps(controllers)
pickled_switches=pickle.dumps(switches)


pickled_c1=pickle.dumps(c1)
pickled_c2=pickle.dumps(c2)

mac_to_port={}
pickled_mac_to_port=pickle.dumps(mac_to_port)

r.set("mac_to_port",pickled_mac_to_port)

r.set("controllers",pickled_controllers)
r.set("c1",pickled_c1)
r.set("c2",pickled_c2)
r.set("switches",pickled_switches)



while True:
    ctrls=pickle.loads(r.get("controllers"))
    ctrls_db={}
    print("current MAC table:")
    print("---------------------------------------------------------------------")
    mac_to_port=pickle.loads(r.get("mac_to_port"))
    print(mac_to_port)
    print("---------------------------------------------------------------------")
    for i in range(len(controllers)):
        ctrls_db["c"+str(i+1)]=pickle.loads(r.get("c"+str(i+1)))
    for controller in ctrls.values():
        print("---------------------------------------------------------------------")
        print("packet in count data for controller "+controller['name'])
        
        
        for switch in ctrls_db[controller['name']]['switches'].values():
            switch_name=switch['name']
            packet_in_count=switch['packet_in_count']
            print("Switch "+switch_name+" has packet count "+str(packet_in_count))
        print("---------------------------------------------------------------------")
    time.sleep(10)

        