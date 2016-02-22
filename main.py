#!/bin/python

import thread
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

try:
    thread.start_new_thread( start_tcp_server, ("Server", ) )
    time.sleep(2)
    thread.start_new_thread( start_udp_server, ("Server", ) )
    time.sleep(2)
    thread.start_new_thread( start_client, ("Client", ) )
except:
    print "Error: unable to start thread"
       
while 1:
    pass
