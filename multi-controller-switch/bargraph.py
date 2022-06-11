import numpy as np
import matplotlib.pyplot as plt
import sys
 

f=open("runtime_data.txt","r")

lines=f.readlines()

random=[]
bestfit=[]
thresholds=[]
time_arr=[]

plot=sys.argv[2]

time=lines[0].strip().split()[3]
threshold=lines[0].strip().split()[1]



for line in lines:
    line=line.strip()
    arr=line.split(" ")
    algo=arr[0]
    thresh=int(arr[1])
    migration_count=int(arr[2])
    t=int(arr[3])
    if algo=="random":
        random.append(migration_count)
        thresholds.append(thresh)
        time_arr.append(t)
    elif algo=="bestfit":
        bestfit.append(migration_count)




print(random)
print(bestfit)
print(thresholds)

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(20, 16))
 
# set height of bar
# IT = [12, 30, 1, 8, 22]
# ECE = [28, 6, 16, 5, 10]
# CSE = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
br1 = np.arange(len(random))
br2 = [x + barWidth for x in br1]
 
# Make the plot
plt.bar(br1, random, color ='b', width = barWidth,
        edgecolor ='grey', label ='Random')
plt.bar(br2, bestfit, color ='g', width = barWidth,
        edgecolor ='grey', label ='Bestfit')

 
# Adding Xticks
if plot=="threshold":
        plt.xlabel('Threshold', fontweight ='bold', fontsize = 20)
        plt.xticks([r + barWidth for r in range(len(random))],
        thresholds,fontsize = 20)
        plt.figtext(.5, .9, "Time = "+time+"s",fontsize=20)

elif plot=="time":
        plt.xlabel('Time', fontweight ='bold', fontsize = 20)
        plt.xticks([r + barWidth for r in range(len(random))],
        time_arr,fontsize = 20)
        plt.figtext(.5, .9, "Threshold = "+threshold+" PACKET_IN count",fontsize=20)

plt.ylabel('Migrations', fontweight ='bold', fontsize = 20)

plt.yticks(fontsize = 20)
 
plt.legend(fontsize=20)
plt.savefig(sys.argv[1])