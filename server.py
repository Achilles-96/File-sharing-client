# server.py

import socket                   # Import socket module
import os
import time
import mimetypes
import hashlib
from datetime import datetime
import glob
import re

def md5(fname):
    hash_value = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()

class udp_server:

    def init(self,ip):
        port = 60001
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        return s

    def runServer(self,ip):
        s = self.init(ip)
        print 'UDP server listening....'

        while True:
            data, addr = s.recvfrom(1024)
            print data + 'In server'
            if data == 'Hello server':
                s.sendto('Hello Client', addr)
            if "File List" in data:
                if "shortlist" in data:
                    try:
                        data_arr = data.split('?')
                        time_l = datetime.strptime(data_arr[1].strip(), "%a %b %d %H:%M:%S %Y")
                        time_r = datetime.strptime(data_arr[2].strip(), "%a %b %d %H:%M:%S %Y")
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]
                        for f in files:
                            created_time = time.ctime(os.path.getctime(f))
                            act_time = datetime.strptime(created_time, "%a %b %d %H:%M:%S %Y")
                            if act_time <= time_r and act_time >= time_l:
                                s.sendto(f + '\n', addr)
                        s.sendto('#END#',addr)
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'

                if "longlist" in data:
                    try:
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]
                        for f in files:
                            statinfo = os.stat(f)
                            size = str(statinfo.st_size)
                            modified_time = time.ctime(os.path.getmtime(f))
                            created_time = time.ctime(os.path.getctime(f))
                            type_of_file, encoding = mimetypes.guess_type(f,True)
                            if type_of_file:
                                s.sendto(f + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + type_of_file + '\n', addr)  #send file list to server
                            else:
                                s.sendto(f + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + 'None' + '\n', addr)  #send file list to server
                        s.sendto('#END#',addr)
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'

                if "regex" in data:
                    try:
                        invalid = False
                        regex = data.split('?')[1].strip()
                        try:
                            re.search(regex,"")
                        except Exception,e:
                            invalid = True
                            print 'Invalid regex'
                        if not invalid:
                            files = [f for f in os.listdir('.') if os.path.isfile(f)]
                            for f in files:
                                if re.search(regex,f):
                                    s.sendto(f + '\n', addr)
                        s.sendto('#END#', addr)
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        continue

            if "Select File" in data:
                try:
                    command,value = data.split('?')
                    value=value.strip()
                    if os.path.isfile(value):
                        filename=value
                        statinfo = os.stat(filename)
                        size = str(statinfo.st_size)
                        modified_time = time.ctime(os.path.getmtime(filename))
                        created_time = time.ctime(os.path.getctime(filename))
                        hash_value = md5(filename)
                        s.sendto(filename+'?'+size+'?'+modified_time+'?'+hash_value+'?', addr)
                        f = open(filename,'rb')
                        l = f.read(1024)
                        while (l):
                            s.sendto(l, addr)
                            l = f.read(1024)
                        f.close()
                        print('Done sending')
                    else:
                        conn.send("#101")
                    s.sendto('#END#',addr)
                except Exception,e:
                    print str(e) + ' : An error occured while fetching the file, make sure you enter the correct command'
            
            if "Hash" in data:
                try:
                    if "single" in data:
                        command1,filename = data.split('?')
                        filename = filename.strip()
                        if os.path.isfile(filename):
                            s.sendto(filename + ' => ' + md5(filename) + ', ' + time.ctime(os.path.getmtime(filename)), addr)
                        else:
                            s.sendto("#101", addr)
                        s.sendto('#END#',addr)
                    elif "all" in data:
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]
                        for f in files:
                            s.sendto(f + ' => ' + md5(f) + ', ' + time.ctime(os.path.getmtime(f)) + '\n', addr)
                        s.sendto('#END#',addr)
                except Exception,e:
                    print str(e) + ' : An error occured while getting the hash of the file(s), make sure you enter the correct command'


class tcp_server:

    def init(self,ip):
        port = 60000                    # Reserve a port for your service.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()     # Get local machine name
        s.bind((ip, port))            # Bind to the port
        s.listen(5)                     # Now wait for client connection.
        return s

    def runServer(self,ip):
        s = self.init(ip)
        print 'TCP server listening....'

        while True:
            conn, addr = s.accept()     # Establish connection with client.
            print 'Got connection from', addr
            data = conn.recv(1024)
            print('Server received', repr(data))

            if data=="Hello server!":
                conn.send("Hello client!")

            if "File List" in data:
                if "shortlist" in data:
                    try:
                        data_arr = data.split('?')
                        time_l = datetime.strptime(data_arr[1].strip(), "%a %b %d %H:%M:%S %Y")
                        time_r = datetime.strptime(data_arr[2].strip(), "%a %b %d %H:%M:%S %Y")
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]
                        for f in files:
                            created_time = time.ctime(os.path.getctime(f))
                            act_time = datetime.strptime(created_time, "%a %b %d %H:%M:%S %Y")
                            if act_time <= time_r and act_time >= time_l:
                                conn.send(f + '\n')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'

                if "longlist" in data:
                    try:
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]
                        for f in files:
                            statinfo = os.stat(f)
                            size = str(statinfo.st_size)
                            modified_time = time.ctime(os.path.getmtime(f))
                            created_time = time.ctime(os.path.getctime(f))
                            type_of_file, encoding = mimetypes.guess_type(f,True)
                            if type_of_file:
                                conn.send(f + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + type_of_file + '\n')  #send file list to server
                            else:
                                conn.send(f + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + 'None' + '\n')  #send file list to server
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'

                if "regex" in data:
                    try:
                        invalid = False
                        regex = data.split('?')[1].strip()
                        try:
                            re.search(regex,"")
                        except Exception,e:
                            invalid = True
                            print 'Invalid regex'
                        if not invalid:
                            files = [f for f in os.listdir('.') if os.path.isfile(f)]
                            for f in files:
                                if re.search(regex,f):
                                    conn.send(f + '\n')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        continue

            if "Select File" in data:
                try:
                    command,value = data.split('?')
                    value=value.strip()
                    if os.path.isfile(value):
                        filename=value
                        statinfo = os.stat(filename)
                        size = str(statinfo.st_size)
                        modified_time = time.ctime(os.path.getmtime(filename))
                        created_time = time.ctime(os.path.getctime(filename))
                        hash_value = md5(filename)
                        conn.send(filename+'?'+size+'?'+modified_time+'?'+hash_value+'?')
                        f = open(filename,'rb')
                        l = f.read(1024)
                        while (l):
                            conn.send(l)
                            l = f.read(1024)
                        f.close()
                        print('Done sending')
                    else:
                        conn.send("#101")
                except Exception,e:
                    print str(e) + ' : An error occured while fetching the file, make sure you enter the correct command'

            if "Hash" in data:
                try:
                    if "single" in data:
                        command1,filename = data.split('?')
                        filename = filename.strip()
                        if os.path.isfile(filename):
                            conn.send(filename + ' => ' + md5(filename) + ', ' + time.ctime(os.path.getmtime(filename)))
                        else:
                            conn.send("#101")
                    elif "all" in data:
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]
                        for f in files:
                            conn.send(f + ' => ' + md5(f) + ', ' + time.ctime(os.path.getmtime(f)) + '\n')
                except Exception,e:
                    print str(e) + ' : An error occured while getting the hash of the file(s), make sure you enter the correct command'
            
            conn.close()

# Error codes
# 101 for file not found

def tcp_main(ip):
    server = tcp_server()
    server.runServer(ip)

def udp_main(ip):
    server = udp_server()
    server.runServer(ip)
