# client.py

import socket                   # Import socket module

class udp_client:

    def connect(self, ip):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        return s

    def send(self,message, file_request, ip):
        try:
            s =  self.connect(ip)
        except Exception, e:
            print 'Failed to create socket'
            return
        receiving = True
        data = ""
        validity = True

        s.sendto(message, ( ip, 60001))

        if file_request:
            try:
                with open('temper1' + message.split(':')[1].strip(), 'wb') as f:
                    while receiving:
                        data, addr = s.recvfrom(1024)
                        if data == '#END#':
                            receiving = False
                            break
                        if data == "#101":
                            validity = False
                        if not data:
                            break
                        # write data to a file
                        if validity == True:
                            print data
                            f.write(data)
                f.close()
                s.close()
                if validity:
                    return "File read"
                else:
                    return "File not found"
            except Exception,e:
                print e
                print 'Unable to fetch file from server, please enter the correct command'
        else:
            try:
                while receiving:
                    data_cur, addr = s.recvfrom(1024)
                    if data_cur == '#END#':
                        receiving = False
                    data += data_cur
                s.close()
                return data
            except Exception,e:
                print 'Unable to fetch data from server'


class tcp_client:
    
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
            try:
                with open('temper' + message.split(':')[1].strip(), 'wb') as f:
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
            except Exception,e:
                print 'Unable to fetch file from server, please enter the correct command'

        else:
            try:
                while receiving:
                    data_cur = s.recv(1024)
                    if not data_cur:
                        receiving = False
                    data += data_cur
                s.close()
                return data
            except Exception,e:
                print 'Unable to fetch data from server'

def main(ip):
    connect_tcp = tcp_client()
    connect_udp = udp_client()
    while True:
        print '1.TCP 2.UDP'
        protocol = input()
        input_raw = raw_input()
        if 'File List shortlist' in input_raw:
            if protocol == 1:
                res = connect_tcp.send("File List shortlist ,Wed Feb 10 15:51:38 2016,Wed Feb 10 15:51:54 2016",False, ip)
            elif protocol == 2:
                res = connect_udp.send("File List shortlist ,Wed Feb 10 15:51:38 2016,Wed Feb 10 15:51:54 2016",False, ip)
            if res:
                print res
            else:
                print 'Failed to fetch shorlist'
        if 'File List longlist' in input_raw:
            if protocol == 1:
                res = connect_tcp.send("File List longlist",False, ip)
            elif protocol == 2:
                res = connect_udp.send("File List longlist",False, ip)
            if res:
                print res
            else:
                print 'Failed to fetch longlist'
        if 'File List regex' in input_raw:
            if protocol == 1:
                res = connect_tcp.send("File List regex",False, ip)
            elif protocol == 2:
                res = connect_udp.send("File List regex",False, ip)
            if res:
                print res
            else:
                print 'Failed to fetch regex'
        if 'Select File' in input_raw:
            if protocol == 1:
                res = connect_tcp.send(input_raw,True, ip)
            elif protocol == 2:
                res = connect_udp.send(input_raw,True, ip)
            if res:
                print res
            else:
                print 'Failed to fetch file'
