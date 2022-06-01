

threshold=30

switches={
    1:{
        "name":"s1",
        "master":"c1",
    },
    2:{
        "name":"s2",
        "master":"c1",
    },
    3:{
        "name":"s3",
        "master":"c1",
    },
    4:{
        "name":"s4",
        "master":"c1",
    },
    5:{
        "name":"s5",
        "master":"c2",
    },
    6:{
        "name":"s6",
        "master":"c2",
    },
}



controllers={
    1:{ 
        "id":1,
        "name":"c1",
        "port":"6633",
        },
    2:{
        "id":2,
        "name":"c2",
        "port":"6634",  
    }
}

c1={
    
    "id":1,
    "name":"c1",
    "port":"6633",
    "switches":{
        1:{
            "name":"s1",
            "packet_in_count":0
        },
        2:{
            "name":"s2",
            "packet_in_count":0
        },
        3:{
            "name":"s3",
            "packet_in_count":0
        },
        4:{
            "name":"s4",
            "packet_in_count":0
        },
       5:{
            "name":"s5",
            "packet_in_count":0
        },
        6:{
            "name":"s6",
            "packet_in_count":0
        },
    }
}

c2={
    
    "id":2,
    "name":"c2",
    "port":"6634",
    "switches":{
        1:{
            "name":"s1",
            "packet_in_count":0
        },
        2:{
            "name":"s2",
            "packet_in_count":0
        },
        3:{
            "name":"s3",
            "packet_in_count":0
        },
        4:{
            "name":"s4",
            "packet_in_count":0
        },
        5:{
            "name":"s5",
            "packet_in_count":0
        },
        6:{
            "name":"s6",
            "packet_in_count":0
        },
       
    }
}

