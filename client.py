# client.py

import socket                   # Import socket module
import sys
import datetime
import time
import os

class udp_client:

    def connect(self, ip):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        return s

    def send(self,message, file_request, ip, directory):
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
                with open(os.path.join(directory,'udp' + message.split('?')[1].strip()), 'wb') as f:
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

    def send(self, message, file_request, ip, directory):
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
                with open(os.path.join(directory,'tcp' + message.split('?')[1].strip()), 'wb') as f:
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

def main(ip, directory):
    connect_tcp = tcp_client()
    connect_udp = udp_client()
    history_file = open('history', 'a+')
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
            history_file.close()
            sys.exit()
        input_raw = raw_input()
        if 'IndexGet shortlist' in input_raw:
            history_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\t' + input_raw + '\n')
            inputs = input_raw.split(' ')
            command_str = 'IndexGet shortlist ?' + inputs[2] + ' ' + inputs[3] + ' ' + inputs[4] + ' ' + inputs[5] + ' ' + inputs[6]  + ' ? ' + inputs[7] + ' ' + inputs[8] + ' ' + inputs[9] + ' ' + inputs[10] + ' ' + inputs[11]
            if protocol == 1:
                #IndexGet shortlist Wed Feb 10 15:51:38 2016 Wed Feb 10 15:51:54 2017
                res = connect_tcp.send(command_str, False, ip, directory)
            elif protocol == 2:
                res = connect_udp.send(command_str, False, ip, directory)
            if res:
                print res
            else:
                print 'No files present or failed to fetch shortlist'
        if 'IndexGet longlist' in input_raw:
            history_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\t' + input_raw + '\n')
            if protocol == 1:
                res = connect_tcp.send("IndexGet longlist", False, ip, directory)
            elif protocol == 2:
                res = connect_udp.send("IndexGet longlist", False, ip, directory)
            if res:
                print res
            else:
                print 'No files present or failed to fetch longlist'
        if 'IndexGet regex' in input_raw:
            history_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\t' + input_raw + '\n')
            command_str = 'IndexGet regex ?' + input_raw.split(' ')[2]
            if protocol == 1:
                res = connect_tcp.send(command_str, False, ip, directory)
            elif protocol == 2:
                res = connect_udp.send(command_str, False, ip, directory)
            if res:
                print res
            else:
                print 'No files present or failed to fetch regex'
        if 'FileDownload' in input_raw:
            history_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\t' + input_raw + '\n')
            command_str = 'FileDownload ? '
            cnt = 0
            for com in input_raw.split(' '):
                if cnt >= 1:
                    command_str += com
                cnt += 1
            if protocol == 1:
                res = connect_tcp.send(command_str, True, ip, directory)
            elif protocol == 2:
                res = connect_udp.send(command_str, True, ip, directory)
            if res:
                print res
            else:
                print 'Failed to fetch file'
        if 'FileHash' in input_raw:
            history_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\t' + input_raw + '\n')
            command_str = 'FileHash ' + input_raw.split(' ')[1] + ' ? '
            cnt = 0
            for com in input_raw.split(' '):
                if cnt >= 2:
                    command_str += com
                cnt += 1
            if protocol == 1:
                res = connect_tcp.send(command_str, False, ip, directory)
            elif protocol == 2:
                res = connect_udp.send(command_str, False, ip, directory)
            if res:
                print res
            else:
                print 'Failed to get hash'

