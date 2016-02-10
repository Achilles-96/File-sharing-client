# client.py

import socket                   # Import socket module

class Client:
    
    def connect(self):
        s = socket.socket()
        print ('connecting to server')
        s.connect((socket.gethostname(),60000))
        return s

    def send(self, message, file_request):
        s = self.connect()
        receiving = True
        data = ""
        
        s.send(message)
        
        if file_request:
            with open('received_file', 'wb') as f:
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
            s.close()
            return "File read"

        else:    
            while receiving:
                data_cur = s.recv(1024)
                if not data_cur:
                    receiving = False
                data += data_cur
            s.close()
            return data


def main():
    connect = Client()
    print connect.send("File List",False)
    print connect.send("File List",False)
    print connect.send("Select File: 8",True)

main()
