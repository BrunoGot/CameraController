#########Houdini connection##################"
import time
import socket
from struct import pack

class HoudiniSender():
    """little Houdini server to send datas to chops
    Open a houdini socket and pipe values
    """

    def __init__(self, ip, port):
        print("init houdini sender")
        #socket
        self.ip = ip
        self.port = port

        #PipeHoudini
        self.esc = chr(170)
        self.nul = chr(0)

    def sendReset(self, conn):
        conn.send(pack('cccccccc', self.esc, self.nul, self.esc, self.nul, self.esc, self.nul, self.esc, self.nul))

    def send(self, conn, value):
        for ch in value:
            if ch == self.esc:
                conn.send(ch)
            conn.send(ch)

    def sendCurrentValues(self, channelCount, samples):
        commandType = 1

        # send command type
        self.pipe_socket.send(pack('>Q', commandType))

        # send channelCount
        self.pipe_socket.send(pack('>Q', channelCount))  # packed as unsigned long long integer > 8bytes

        # send samples
        for s in samples:
            self.send(self.pipe_socket, pack('>d', s))  # packed as double float > 8bytes

    def activate_server(self, ip, port):
        print("start houdini server at ip = "+ip+" port = "+str(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(1)
        self.pipe_socket, self.pipe_addr = s.accept()  # conn is the socket to communicate with the client
        print('connection established')  # this is where i'm stuck
        #return conn

    def run(self):
        self.activate_server(self.ip, self.port)

if __name__ == "__main__":
    ip = "192.168.1.50"
    port = 10086
    hs = HoudiniSender(ip, port)
