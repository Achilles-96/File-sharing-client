# server.py

import socket                   # Import socket module
import os
import time
import mimetypes
import hashlib
from datetime import datetime
import glob

def md5(fname):
    hash_value = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()

class Server:

    def init(self,ip):
        port = 60000                    # Reserve a port for your service.
        s = socket.socket()             # Create a socket object
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()     # Get local machine name
        s.bind((ip, port))            # Bind to the port
        s.listen(5)                     # Now wait for client connection.
        return s

    def runServer(self,ip):
        s = self.init(ip)
        print 'Server listening....'

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
                        print 'An error occured while fetching the filelist, make sure you enter the correct command'

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
                        print 'An error occured while fetching the filelist, make sure you enter the correct command'

                if "regex" in data:
                    try:
                        regex = data.split('?')[1]
                        files = glob.glob(regex.strip())
                        for f in files:
                            conn.send(f + '\n')
                    except Exception,e:
                        print 'An error occured while fetching the filelist, make sure you enter the correct command'

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
                    print 'An error occured while sending the file, make sure you enter the correct command'
            
            conn.close()

# Error codes
# 101 for file not found

def main(ip):
    server = Server()
    server.runServer(ip)
