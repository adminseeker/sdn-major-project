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
sum_load=[]
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
    sum_load.append(int(load))

i=0
for line in f2_lines:
    load=line.strip().split(" ")[1]
    c2_load.append(int(load))
    sum_load[i]+=int(load)
    i=i+1

i=0
for line in f3_lines:
    load=line.strip().split(" ")[1]
    c3_load.append(int(load))
    sum_load[i]+=int(load)
    i=i+1

# print(sum_load)

c1_load_percent=[]
c2_load_percent=[]
c3_load_percent=[]

for i in range(len(sum_load)):
    c1_load_p=(c1_load[i]/sum_load[i])*100
    c1_load_percent.append(c1_load_p)
    c2_load_p=(c2_load[i]/sum_load[i])*100
    c2_load_percent.append(c2_load_p)
    c3_load_p=(c3_load[i]/sum_load[i])*100
    c3_load_percent.append(c3_load_p)

# print(c1_load_percent)

# plot lines
plt.plot(intervals, c1_load_percent, label = "c1")
plt.plot(intervals, c2_load_percent, label = "c2")
plt.plot(intervals, c3_load_percent, label = "c3")
# plt.plot(intervals, threshold_arr, label = "threshold")
plt.xlabel('Time', fontweight ='bold', fontsize = 10)
plt.ylabel('load (%)', fontweight ='bold', fontsize = 10)


plt.legend()
plt.savefig(sys.argv[1])