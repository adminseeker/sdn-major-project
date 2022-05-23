from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import random
from ryu.lib import hub
import redis
import pickle
import json
import sys
import os

r=redis.Redis(host="127.0.0.1",port=6379)

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = pickle.loads(r.get("mac_to_port"))
        self.datapaths = {}
        self.packet_in_count=0
        
        hub.spawn(self.role_requester)
        hub.spawn(self.monitor_packets)
        self.controllers=pickle.loads(r.get("controllers"))
        self.switches=pickle.loads(r.get("switches"))
        (self.controller_name,self.controller_id)=self.get_current_controller()
        self.controller=pickle.loads(r.get(self.controller_name))
        


    def send_role_request(self, datapath, role, gen_id):
        ofp_parser = datapath.ofproto_parser
        msg = ofp_parser.OFPRoleRequest(datapath, role, gen_id)
        datapath.send_msg(msg)

    def role_requester(self):
        self.logger.info("started role_requester")
        while True:
            self.logger.info("requesting role.....")
            print("------------------------------------------------------------------")
            hub.sleep(5)
            self.switches=pickle.loads(r.get("switches"))
            if len(self.datapaths) !=0:
                    for datapath in self.datapaths.values():
                        role=""
                        if self.switches[datapath.id]['master']==self.controller_name:
                            role="master"
                        else:
                            role="slave"
                        if role=="slave":
                            self.send_role_request(datapath, datapath.ofproto.OFPCR_ROLE_SLAVE, 0)
                        elif role=="master":
                            self.send_role_request(datapath, datapath.ofproto.OFPCR_ROLE_MASTER, 0)
            print("------------------------------------------------------------------")
            
                    
        

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        self.datapaths[datapath.id] = datapath
       
        # print(sys.argv[-1])
        # install table-miss flow entry
    

    
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)


    def get_current_controller(self):
        # print(sys.argv)
        port=""
        for i in sys.argv:
            if i=="--ofp-tcp-listen-port":
                port=sys.argv[sys.argv.index(i)+1]
                break
        for i in self.controllers.values():
            if i['port']==port:
                return (i['name'],i['id'])

                
    def monitor_packets(self):
        self.logger.info("packet monitoring started")
        while True:
            print("------------------------------------------------------------------")
            hub.sleep(10)
            print("updating packet counters....")
            
            pickled_ctrl=pickle.dumps(self.controller)
            r.set(self.controller_name,pickled_ctrl)
            print("------------------------------------------------------------------")
            

    def add_flow(self, datapath, priority, match, actions, buffer_id=None,idle=0, hard=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath,idle_timeout=idle,hard_timeout=hard, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath,idle_timeout=idle,hard_timeout=hard, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
                

    

    
    @set_ev_cls(ofp_event.EventOFPRoleReply, MAIN_DISPATCHER)
    def on_role_reply(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        role = msg.role
        gen_id = msg.generation_id

        
        # if role == ofp.OFPCR_ROLE_MASTER:
        #     print('This Controller is master for switch s'+str(dp.id))
        # elif role == ofp.OFPCR_ROLE_SLAVE:
        #     print('This Controller is slave for switch s'+str(dp.id))
        # else:
        #     # never occur
        #     pass
    


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
       
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
    
        dpid = format(datapath.id, "d").zfill(16)

        self.controller['switches'][datapath.id]['packet_in_count']=self.controller['switches'][datapath.id]['packet_in_count']+1
        # print(self.controller)
      
        print("update from controller "+self.controller['name'])
        
        # self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.

        self.mac_to_port = pickle.loads(r.get("mac_to_port"))


        self.mac_to_port.setdefault(dpid, {})
            
        
        
        self.mac_to_port[dpid][src] = in_port



        r.set("mac_to_port",pickle.dumps(self.mac_to_port))
        


        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id,idle=5, hard=10)
                return
            else:
                self.add_flow(datapath, 1, match, actions,idle=5, hard=10)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)