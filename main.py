import thread
import time
import server
import client

def start_server(threadName):
    print 'Started server'
    server.main()

def start_client(threadName):
    print 'Started client'
    client.main()

try:
    thread.start_new_thread( start_server, ("Server", ) )
    time.sleep(2)
    thread.start_new_thread( start_client, ("Client", ) )
except:
    print "Error: unable to start thread"
       
while 1:
    pass
