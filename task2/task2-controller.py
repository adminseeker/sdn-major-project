from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import random


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}
        self.subscriptions={"PLATINUM":["00:00:00:00:00:01"],
                            "GOLD":["00:00:00:00:00:02"],
                            "SILVER":["00:00:00:00:00:03"]
                            }


    def send_role_request(self, datapath, role, gen_id):
        role = datapath.ofproto.OFPCR_ROLE_MASTER
        ofp_parser = datapath.ofproto_parser
        msg = ofp_parser.OFPRoleRequest(datapath, role, gen_id)
        datapath.send_msg(msg)


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        self.datapaths[datapath.id] = datapath

        # install table-miss flow entry
        self.send_role_request(datapath, ofproto.OFPCR_ROLE_MASTER, 0)
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

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
                

    
    def handle_platinum_connections(self,idle=5,hard=10):
        host=self.subscriptions["PLATINUM"][0]
        server="00:00:00:00:00:04"
        

        path=random.choice([1,2])
        if path==1:
            print("PLATINUM CONNECTION, SELECTED PATH S1<->S2<->S3")
            def s1_flows():
                datapath=self.datapaths[1]
                parser = datapath.ofproto_parser

                in_port=4
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s2_flows():
                datapath=self.datapaths[2]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s3_flows():
                datapath=self.datapaths[3]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=4
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            s1_flows()
            s2_flows()
            s3_flows()
        elif path==2:
            print("PLATINUM CONNECTION, SELECTED PATH S1<->S4<->S3")
            def s1_flows():
                datapath=self.datapaths[1]
                parser = datapath.ofproto_parser

                in_port=4
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=2
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s4_flows():
                datapath=self.datapaths[4]
                parser = datapath.ofproto_parser

                in_port=2
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s3_flows():
                datapath=self.datapaths[3]
                parser = datapath.ofproto_parser

                in_port=2
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=4
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            s1_flows()
            s4_flows()
            s3_flows()


    def handle_gold_connections(self,idle=5,hard=10):
        host=self.subscriptions["GOLD"][0]
        server="00:00:00:00:00:04"
        

        path=random.choice([1,2])
        if path==1:
            print("GOLD CONNECTION, SELECTED PATH S1<->S7<->S8<->S6<->S3")
            def s1_flows():
                datapath=self.datapaths[1]
                parser = datapath.ofproto_parser
                in_port=5
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=1
                out_port=5            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s7_flows():
                datapath=self.datapaths[7]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=2
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s8_flows():
                datapath=self.datapaths[8]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=2
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            
            def s6_flows():
                datapath=self.datapaths[6]
                parser = datapath.ofproto_parser

                in_port=2
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s3_flows():
                datapath=self.datapaths[3]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=4
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            s1_flows()
            s7_flows()
            s8_flows()
            s6_flows()
            s3_flows()

        elif path==2:
            print("GOLD CONNECTION, SELECTED PATH S1<->S7<->S5<->S6<->S3")
            def s1_flows():
                datapath=self.datapaths[1]
                parser = datapath.ofproto_parser
                in_port=5
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=1
                out_port=5            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s7_flows():
                datapath=self.datapaths[7]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=1
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s5_flows():
                datapath=self.datapaths[5]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=1
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            
            def s6_flows():
                datapath=self.datapaths[6]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s3_flows():
                datapath=self.datapaths[3]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=4
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            s1_flows()
            s7_flows()
            s5_flows()
            s6_flows()
            s3_flows()


    def handle_silver_connections(self,idle=5,hard=10):
        host=self.subscriptions["SILVER"][0]
        server="00:00:00:00:00:04"
        

        path=random.choice([1,2])
        if path==1:
            print("SILVER CONNECTION, SELECTED PATH S1<->S2<->S8<->S6<->S3")
            def s1_flows():
                datapath=self.datapaths[1]
                parser = datapath.ofproto_parser
                in_port=6
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=6            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s2_flows():
                datapath=self.datapaths[2]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=2
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s8_flows():
                datapath=self.datapaths[8]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=2
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            
            def s6_flows():
                datapath=self.datapaths[6]
                parser = datapath.ofproto_parser

                in_port=2
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s3_flows():
                datapath=self.datapaths[3]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=4
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            s1_flows()
            s2_flows()
            s8_flows()
            s6_flows()
            s3_flows()

        elif path==2:
            print("SILVER CONNECTION, SELECTED PATH S1<->S7<->S5<->S4<->S3")
            def s1_flows():
                datapath=self.datapaths[1]
                parser = datapath.ofproto_parser
                in_port=6
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=1
                out_port=6            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s7_flows():
                datapath=self.datapaths[7]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=1
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s5_flows():
                datapath=self.datapaths[5]
                parser = datapath.ofproto_parser

                in_port=3
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=2
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            
            def s4_flows():
                datapath=self.datapaths[4]
                parser = datapath.ofproto_parser

                in_port=1
                out_port=3            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=3
                out_port=1            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

            def s3_flows():
                datapath=self.datapaths[3]
                parser = datapath.ofproto_parser

                in_port=2
                out_port=4            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=server, eth_src=host)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)

                in_port=4
                out_port=2            
                actions = [parser.OFPActionOutput(out_port)]
                match = parser.OFPMatch(in_port=in_port, eth_dst=host, eth_src=server)
                self.add_flow(datapath, 1, match, actions,idle=idle,hard=hard)
            s1_flows()
            s7_flows()
            s5_flows()
            s4_flows()
            s3_flows()
           
        


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

        
        if src in self.subscriptions["PLATINUM"] or dst in self.subscriptions["PLATINUM"]:
            self.handle_platinum_connections()
        if src in self.subscriptions["GOLD"] or dst in self.subscriptions["GOLD"]:
            self.handle_gold_connections()
        if src in self.subscriptions["SILVER"] or dst in self.subscriptions["SILVER"]:
            self.handle_silver_connections()
