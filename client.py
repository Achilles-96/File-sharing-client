# client.py

import socket                   # Import socket module

class Client:
    
    def connect(self,ip):
        s = socket.socket()
        print ('connecting to server')
        s.connect((ip,60000))
        return s

    def send(self, message, file_request, ip):
        try:
            s = self.connect(ip)
        except Exception, e:
            print 'Failed to connect'
            return
        receiving = True
        data = ""
        validity = True

        s.send(message)
        
        if file_request:
            with open('received_file', 'wb') as f:
                while True:
                    data = s.recv(1024)
                    if data == "#101":
                        validity = False
                    if not data:
                        break
                    # write data to a file
                    if validity == True:
                        f.write(data)
            f.close()
            s.close()
            if validity:
                return "File read"
            else:
                return "File not found"

        else:    
            while receiving:
                data_cur = s.recv(1024)
                if not data_cur:
                    receiving = False
                data += data_cur
            s.close()
            return data


def main(ip):
    connect = Client()
    while True:
        input_raw = raw_input()
        if 'File List shortlist' in input_raw:
            res = connect.send("File List shortlist",False, ip)
            if res:
                print res
            else:
                print 'Failed to fetch shorlist'
        if 'File List longlist' in input_raw:
            res = connect.send("File List longlist",False, ip)
            if res:
                print res
            else:
                print 'Failed to fetch longlist'
        if 'File List regex' in input_raw:
            res = connect.send("File List regex",False, ip)
            if res:
                print res
            else:
                print 'Failed to fetch regex'
        if 'Select File' in input_raw:
            res = connect.send(input_raw,True, ip)
            if res:
                print res
            else:
                print 'Failed to fetch file'
