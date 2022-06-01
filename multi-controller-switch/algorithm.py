import random


c1={'id': 1, 'name': 'c1', 'port': '6633', 'switches': {1: {'name': 's1', 'packet_in_count': 0}, 2: {'name': 's2', 'packet_in_count': 0}, 3: {'name': 's3', 'packet_in_count': 120}, 4: {'name': 's4', 'packet_in_count': 0}, 5: {'name': 's5', 'packet_in_count': 0}, 6: {'name': 's6', 'packet_in_count': 0}}}

c2={'id': 2, 'name': 'c2', 'port': '6634', 'switches': {1: {'name': 's1', 'packet_in_count': 10}, 2: {'name': 's2', 'packet_in_count': 0}, 3: {'name': 's3', 'packet_in_count': 0}, 4: {'name': 's4', 'packet_in_count': 0}, 5: {'name': 's5', 'packet_in_count': 0}, 6: {'name': 's6', 'packet_in_count': 0}}}

c3={'id': 3, 'name': 'c3', 'port': '6635', 'switches': {1: {'name': 's1', 'packet_in_count': 10}, 2: {'name': 's2', 'packet_in_count': 0}, 3: {'name': 's3', 'packet_in_count': 0}, 4: {'name': 's4', 'packet_in_count': 0}, 5: {'name': 's5', 'packet_in_count': 0}, 6: {'name': 's6', 'packet_in_count': 0}}}

def total_packet_in_count(controller):
    sum=0
    for switch in controller['switches'].values():
        sum+=switch['packet_in_count']
    return sum


def exceeds_threshold(threshold,sum):
    if sum>=threshold:
        return True
    return False

def get_available_controllers(controllers,threshold):
    available_controllers={}
    busy_controllers={}
    for c in controllers:
        sum=total_packet_in_count(c)
        if not exceeds_threshold(threshold,sum):
            available_controllers[c['name']]=sum
        else:
            busy_controllers[c['name']]=sum
    available_controllers=dict(sorted(available_controllers.items(), key=lambda item: item[1]))
    busy_controllers=dict(sorted(busy_controllers.items(), key=lambda item: item[1]))
    return available_controllers,busy_controllers
    
def select_busy_switch(controller):
    busy_switches={}
    result={}
    for switch in controller['switches'].values():
        busy_switches[switch['name']]=switch['packet_in_count']
    busy_switches=dict(sorted(busy_switches.items(), key=lambda item: item[1]))
    result[list(busy_switches.keys())[-1]]=busy_switches[list(busy_switches.keys())[-1]]
    return result

def select_migration(controllers,threshold):
    available_controllers,busy_controllers=get_available_controllers(controllers,threshold)
    err={"msg":[]}
    if len(busy_controllers)==0:
        err["msg"].append("No busy controllers")
        return (err,err)
    if len(available_controllers)==0:
        err["msg"].append("No available controllers")
        return (err,err)
    rand_busy=random.randint(0,len(busy_controllers)-1)
    rand_available=random.randint(0,len(available_controllers)-1)
    busy_ctrl={}
    available_ctrl={}
    busy_ctrl[list(busy_controllers.keys())[rand_busy]]=busy_controllers[list(busy_controllers.keys())[rand_busy]]
    available_ctrl[list(available_controllers.keys())[rand_available]]=available_controllers[list(available_controllers.keys())[rand_available]]
    busy_controller={}
    available_controller={}
    for c in controllers:
        if c['name']==list(busy_ctrl.keys())[0]:
            busy_controller=c
        if c['name']==list(available_ctrl.keys())[0]:
            available_controller=c
    busy_switch=select_busy_switch(busy_controller)
    migration={}
    premigration={}
    migration[list(busy_switch.keys())[0]]=list(available_ctrl.keys())[0]
    premigration[list(busy_switch.keys())[0]]=list(busy_ctrl.keys())[0]

    
        
    return (premigration,migration)

# print(select_migration([c1,c2,c3],100))