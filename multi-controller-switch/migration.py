import pickle
import algorithm
import config

def handle_migration(red,ctrls,swths,threshold):
    ctrls_arr=list(ctrls.values())
    premigration,migration=algorithm.select_migration(ctrls_arr,threshold)
    
    if list(premigration.keys())[0]=="msg" or list(migration.keys())[0]=='msg':
        print(premigration)
        return
    
    

    premigration_controller=list(premigration.values())[0]
    migration_switch=list(migration.keys())[0]
    migration_controller=list(migration.values())[0]

    filename=""
    if algorithm.selected_algorithm=="random":
        filename="random_migrations.txt"
    elif algorithm.selected_algorithm=="bestfit":
        filename="bestfit_migrations.txt"
    
    f = open(filename,"a")
    f.write(algorithm.selected_algorithm + " migration of switch "+migration_switch+" from controller "+premigration_controller+" to controller "+migration_controller+" at threshold: "+str(config.threshold)+" PACKET_IN Counts in runtime: " +str(config.run_time) +" seconds\n")
    f.close()

    s=pickle.loads(red.get('switches'))
    for i in s.values():
        if i['name']==migration_switch:
            i['master']=migration_controller
            break
    
    old_controller=ctrls[premigration_controller]
    for i in old_controller['switches'].values():
        if i['name']==migration_switch:
            i['packet_in_count']=0
            break
    pickled_old_controller=pickle.dumps(old_controller)
    a=red.set(premigration_controller,pickled_old_controller)
    pickled_s=pickle.dumps(s)
    red.set("switches",pickled_s)

# handle_migration(r,dict_ctrls,switches,threshold)
