"""
server get the datas from the hardware
"""
import socket
import houdini_sender as hou_pipe

#connection with the controller
ip = "192.168.1.25"#network.WLAN(network.STA_IF)
udp_port = 10086

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("*bind socket***")
sock.bind((ip, udp_port))
print("*socket binded")

#connection with houdini software
#if sock = true
hou_ip = ip#ip of the software
hou_port = 50556#port of houdini pipe
hou_sender = hou_pipe.HoudiniSender(hou_ip, hou_port)
hou_sender.run()
channelCount = 1
samples = [4.2]
while True:
 data, adrr = sock.recvfrom(1024) #buffer size is 1024 bytes
 print("received message: %s "%data)

 #compute datas
 data = float(data)
 data = round(data, 2)
 samples = [data]
 hou_sender.sendCurrentValues(channelCount,samples)
 #msg = "hello world"

