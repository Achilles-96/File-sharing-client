#!/bin/python

import thread
import time
import server
import client
import sys

def start_server(threadName):
    print 'Started server'
    server.main(sys.argv[1])

def start_client(threadName):
    print 'Started client'
    client.main(sys.argv[2])

try:
    thread.start_new_thread( start_server, ("Server", ) )
    time.sleep(2)
    thread.start_new_thread( start_client, ("Client", ) )
except:
    print "Error: unable to start thread"
       
while 1:
    pass
