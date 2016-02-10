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


def main():
    connect = Client()
    print connect.send("File List shortlist",False)
    print connect.send("File List longlist",False)
    print connect.send("File List regex",False)
    print connect.send("Select File: 8",True)
