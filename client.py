# client.py

import socket                   # Import socket module

class Connect:
    
    def connect(self):
        s = socket.socket()
        print ('connecting to server')
        s.connect((socket.gethostname(),60000))
        return s

    def send(self, message):
        s = self.connect()
        receiving = True
        data = ""

        s.send(message)

        while receiving:
            data_cur = s.recv(1024)
            data += data_cur
            print ('received: ' + data)
            if not data_cur:
                receiving = False
        
        s.close()
        return data

'''with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')'''

def main():
    connect = Connect()
    print connect.send("File List")
    print connect.send("File List")

main()
