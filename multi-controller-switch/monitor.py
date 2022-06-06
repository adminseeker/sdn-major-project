import redis
import pickle
from config import *
import time
import migration


r=redis.Redis(host="127.0.0.1",port=6379)

monitor_time = 10

# Setting values from config.py into redis
pickled_controllers=pickle.dumps(controllers)
pickled_switches=pickle.dumps(switches)
pickled_threshold=pickle.dumps(threshold)

pickled_c1=pickle.dumps(c1)
pickled_c2=pickle.dumps(c2)
pickled_c3=pickle.dumps(c3)

mac_to_port={}
pickled_mac_to_port=pickle.dumps(mac_to_port)

r.set("mac_to_port",pickled_mac_to_port)

r.set("controllers",pickled_controllers)
r.set("c1",pickled_c1)
r.set("c2",pickled_c2)
r.set("c3",pickled_c3)
r.set("switches",pickled_switches)
r.set("threshold",pickled_threshold)


# For every monitor_time seconds, monitor from database and perform migration
while True:

    # Getting controllers,switches,threshold from redis database
    ctrls=pickle.loads(r.get("controllers"))
    swths=pickle.loads(r.get("switches"))
    thresh=pickle.loads(r.get("threshold"))
    ctrls_db={}
    print("current MAC table:")
    print("---------------------------------------------------------------------")
    mac_to_port=pickle.loads(r.get("mac_to_port"))
    print(mac_to_port)
    print("---------------------------------------------------------------------")
    
    # Populating ctrls_db with redis database (c1,c2.....) 
    for i in range(len(controllers)):
        ctrls_db["c"+str(i+1)]=pickle.loads(r.get("c"+str(i+1)))
    
    # Reading and printing data from redis database
    for controller in ctrls.values():
        print("---------------------------------------------------------------------")
        print("packet in count data for controller "+controller['name'])
        
        # print(ctrls_db)
        for switch in ctrls_db[controller['name']]['switches'].values():
            switch_name=switch['name']
            packet_in_count=switch['packet_in_count']
            print("Switch "+switch_name+" has packet count "+str(packet_in_count))
        print("---------------------------------------------------------------------")
    
    # Start the migration process
    migration.handle_migration(r,ctrls_db,swths,thresh)
    time.sleep(monitor_time)

        