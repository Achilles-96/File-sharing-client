# client.py

import socket                   # Import socket module
import sys

class udp_client:

    def connect(self, ip):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        return s

    def send(self,message, file_request, ip):
        try:
            s =  self.connect(ip)
        except Exception, e:
            print str(e) + ' : Failed to create socket'
            return
        receiving = True
        data = ""
        validity = True
        header = True

        s.sendto(message, ( ip, 60001))

        if file_request:
            try:
                with open('temper1' + message.split('?')[1].strip(), 'wb') as f:
                    while receiving:
                        data, addr = s.recvfrom(1024)
                        if data == '#END#':
                            receiving = False
                            break
                        if data == "#101":
                            validity = False
                        if not data:
                            break
                        if header and len(data.split('?'))>4:
                            print 'Received File'
                            print data.split('?')[0]
                            print data.split('?')[1]
                            print data.split('?')[2]
                            print data.split('?')[3]
                            print 'End of header'
                            f.write(data.split('?')[4])
                            header = False
                        elif validity == True:
                            f.write(data)
                f.close()
                s.close()
                if validity:
                    return "File read"
                else:
                    return "File not found"
            except Exception,e:
                print str(e) + ' : Unable to fetch file from server, please enter the correct command'
        else:
            try:
                while receiving:
                    data_cur, addr = s.recvfrom(1024)
                    if data_cur == '#END#':
                        receiving = False
                        break
                    data += data_cur
                s.close()
                return data
            except Exception,e:
                print str(e) + ' : Unable to fetch data from server'


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
            print str(e) + ' : Failed to connect'
            return
        receiving = True
        data = ""
        validity = True
        header = True

        s.send(message)
        
        if file_request:
            try:
                with open('temper' + message.split('?')[1].strip(), 'wb') as f:
                    while True:
                        data = s.recv(1024)
                        if data == "#101":
                            validity = False
                        if not data:
                            break
                        if header and len(data.split('?'))>4:
                            print 'Received File'
                            print data.split('?')[0]
                            print data.split('?')[1]
                            print data.split('?')[2]
                            print data.split('?')[3]
                            print 'End of header'
                            f.write(data.split('?')[4])
                            header = False
                        elif validity == True:
                            f.write(data)
                        # write data to a file
                f.close()
                s.close()
                if validity:
                    return "File read"
                else:
                    return "File not found"
            except Exception,e:
                print str(e) + ' : Unable to fetch file from server, please enter the correct command'

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
                print str(e) + ' : Unable to fetch data from server'

def main(ip):
    connect_tcp = tcp_client()
    connect_udp = udp_client()
    while True:
        print '1.TCP 2.UDP 3.Quit'
        try:
            protocol = input()
        except Exception,e:
            print str(e) + ' : Please enter a number corresponding to the protocol'
            continue
        if protocol != 1 and protocol != 2 and protocol != 3:
            continue
        if protocol == 3:
            sys.exit()
        input_raw = raw_input()
        if 'File List shortlist' in input_raw:
            if protocol == 1:
                #File List shortlist ? Wed Feb 10 15:51:38 2016 ? Wed Feb 10 15:51:54 2017
                res = connect_tcp.send(input_raw, False, ip)
            elif protocol == 2:
                res = connect_udp.send(input_raw, False, ip)
            if res:
                print res
            else:
                print 'No files present or failed to fetch shortlist'
        if 'File List longlist' in input_raw:
            if protocol == 1:
                res = connect_tcp.send("File List longlist", False, ip)
            elif protocol == 2:
                res = connect_udp.send("File List longlist", False, ip)
            if res:
                print res
            else:
                print 'No files present or failed to fetch longlist'
        if 'File List regex' in input_raw:
            if protocol == 1:
                res = connect_tcp.send(input_raw, False, ip)
            elif protocol == 2:
                res = connect_udp.send(input_raw, False, ip)
            if res:
                print res
            else:
                print 'No files present or failed to fetch regex'
        if 'Select File' in input_raw:
            if protocol == 1:
                res = connect_tcp.send(input_raw, True, ip)
            elif protocol == 2:
                res = connect_udp.send(input_raw, True, ip)
            if res:
                print res
            else:
                print 'Failed to fetch file'
        if 'Hash' in input_raw:
            if protocol == 1:
                res = connect_tcp.send(input_raw, False, ip)
            elif protocol == 2:
                res = connect_udp.send(input_raw, False, ip)
            if res:
                print res
            else:
                print 'Failed to get hash'

