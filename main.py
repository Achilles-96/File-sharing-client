#!/bin/python

from threading import Thread
import time
import server
import client
import sys

def start_tcp_server(threadName):
    print 'Started TCP server'
    server.tcp_main(sys.argv[1])

def start_udp_server(threadName):
    print 'Started UDP server'
    server.udp_main(sys.argv[1])

def start_client(threadName):
    print 'Started client'
    client.main(sys.argv[2])

t1 = Thread( target=start_tcp_server, args=("Server1", ) )
t1.daemon = True
t1.start()
time.sleep(1)
t2 = Thread( target=start_udp_server, args=("Server2", ) )
t2.daemon = True
t2.start()
time.sleep(1)
t3 = Thread( target=start_client, args=("Client", ) )
t3.start()
       
t3.join()
sys.exit()
