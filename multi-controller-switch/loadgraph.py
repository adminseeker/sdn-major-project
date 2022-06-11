import matplotlib.pyplot as plt
import numpy as np
import config
import sys
  
# create data

threshold=config.threshold
intervals=[]
c1_load=[]
c2_load=[]
c3_load=[]
threshold_arr=[]


f1=open("c1_load_data.txt","r")
f2=open("c2_load_data.txt","r")
f3=open("c3_load_data.txt","r")

f1_lines=f1.readlines()
f2_lines=f2.readlines()
f3_lines=f3.readlines()

f1.close()
f2.close()
f3.close()

for line in f1_lines:
    interval=line.strip().split(" ")[2]
    intervals.append(int(interval))
    threshold_arr.append(threshold)
    load=line.strip().split(" ")[1]
    c1_load.append(int(load))

for line in f2_lines:
    load=line.strip().split(" ")[1]
    c2_load.append(int(load))

for line in f3_lines:
    load=line.strip().split(" ")[1]
    c3_load.append(int(load))


# plot lines
plt.plot(intervals, c1_load, label = "c1")
plt.plot(intervals, c2_load, label = "c2")
plt.plot(intervals, c3_load, label = "c3")
plt.plot(intervals, threshold_arr, label = "threshold")
plt.xlabel('Time', fontweight ='bold', fontsize = 10)
plt.ylabel('load (PACKET_IN count)', fontweight ='bold', fontsize = 10)


plt.legend()
plt.savefig(sys.argv[1])