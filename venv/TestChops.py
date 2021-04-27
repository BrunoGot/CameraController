import time
import socket
from struct import pack

class HoudiniSender():

	def __init__(self):
		self.esc = chr(170)
		self.nul = chr(0)

	def sendReset(self, conn):
		conn.send(pack('cccccccc', self.esc, self.nul, self.esc, self.nul, self.esc, self.nul, self.esc, self.nul))

	def send(self, conn, value):
		for ch in value:
			if ch == esc:
				conn.send(ch)
			conn.send(ch)

	def sendCurrentValues(self, conn, channelCount, samples):
		commandType = 1

		#send command type
		conn.send(pack('>Q', commandType))

		#send channelCount
		conn.send(pack('>Q', channelCount)) #packed as unsigned long long integer > 8bytes

		#send samples
		for s in samples:
				print("send datas")
				send(conn, pack('>d', s)) #packed as double float > 8bytes

print("start")
esc = chr(170)
nul = chr(0)

#open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 50556))
s.listen(1)
conn, addr = s.accept()
print 'connection established' #this is where i'm stuck

sendReset(conn)
for o in range(10000):
    print(o)
    channelCount = 1
    samples = [4.2]
    sendCurrentValues(conn, channelCount, samples)

    time.sleep(0.03)

print("end")