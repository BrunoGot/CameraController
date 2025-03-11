"""
server get the datas from the hardware
"""
import socket
import thread
import houdini_sender as hou_pipe
import math


class Server():
    def __init__(self):
        # connection with the controller
        ip = "192.168.43.50"  # network.WLAN(network.STA_IF)
        udp_port = 10086

        self.controller = ControllerHandler(ip, udp_port)
        #send thread to print controller datas
        thread.start_new_thread(self.controller.listen, ())

        # connection with houdini software
        # if sock = true
        hou_ip = ip  # ip of the software
        hou_port = 50556  # port of houdini pipe
        hou_sender = hou_pipe.HoudiniSender(hou_ip, hou_port)
        hou_sender.run()
        channelCount = 3
        while True:
            #print("received message: %s " % data)
            data = self.controller.get_datas()
            # compute datas
            samples = [data.x,data.y,data.z]
            print("send datas to houdini : " + str(data.z))
            hou_sender.sendCurrentValues(channelCount, samples)
            # msg = "hello world"

class ControllerHandler():
    """this class is here to get the signal from the controller part, clean it and compute it """
    def __init__(self, ip, udp_port):
        #open socket to receie datas
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("*bind socket***")
        self.sock.bind((ip, udp_port))
        print("*socket binded")
        #define current data and old data to make some interpolation
        #print(bytearray.deself.sock.recvfrom(1024)[0])
        datas = self.split_datas_to_vector()
        self.__accel = datas[0]
        print("init accel = "+str(self.__accel))
        self.__old_accel = self.__accel
        self.__gyro = datas[1]
        self.__old_gyro = self.__gyro

    def receiv_datas(self):
        """for now datas are reiceved as string like 'Xval,Yval,Zval' """
        raw_datas = self.sock.recvfrom(1024)[0]
        datas = raw_datas.split(',')
        #self.print_controller_datas(datas[5])
        return datas #return x val only for now

    def split_datas_to_vector(self):
        """split the datas in accel and gyro vectors"""
        datas = self.receiv_datas()
        accel = Vector(0,0,0)
        gyro = Vector(0,0,0)
        if len(datas)>=6:
            accel = Vector(datas[0],datas[1],datas[2])
            gyro = Vector(datas[3],datas[4],datas[5])
        return (accel, gyro)

    def print_controller_datas(self, data):
        print("received controller message : " + str(data.y) +"x "+ str(data.x)+"y "+str(data.z)+"z ")

    def smooth_datas(self, new_data,current_data, old_data):
        """ take the new received data, the cureent data like self.__accel, and the buffered datas, make interpolation with it to smooth the datas
        and return an array with the updated values"""
        precision =2
        #interpolate with the old data current data and new data
        #x
        new_data.x = (old_data.x + current_data.x + new_data.x) / 3
        new_data.x = round(new_data.x, precision)
        #y
        new_data.y = (old_data.y + current_data.y + new_data.y) / 3
        new_data.y = round(new_data.y, precision)
        #z
        new_data.z = (old_data.z + current_data.z + new_data.z) / 3
        new_data.z = round(new_data.z, precision)

        old_data = current_data
        current_data = new_data
        #print("smooth_datas : (current_data, old_data) =  "+str((current_data, old_data)))
        return (current_data, old_data)

    def update_datas(self):
        #print("update datas")
        #receive the datas and convert it in vectors0
        datas = self.split_datas_to_vector()
        accel = datas[0]
        """print("accel = "+str(accel))
        print("self.__accel = "+str(self.__accel))
        print("self.__old_accel = "+str(self.__old_accel))"""
        gyro = datas[1]
        # update accel value
        accel_buffers = self.smooth_datas(accel, self.__accel, self.__old_accel)
        self.__accel = accel_buffers[0]
        self.__old_accel = accel_buffers[1]
        # update gyro value
        gyro_buffers = self.smooth_datas(gyro, self.__gyro, self.__old_gyro)
        self.__gyro = gyro#gyro_buffers[0]
        self.__old_gyro = gyro_buffers[1]

    def listen(self):
        while True:
            # buffer size is 1024 bytes
            self.update_datas()
            self.print_controller_datas(self.__gyro)


    def get_datas(self):
        return self.__accel

class Vector():
    def __init__(self,x,y,z):
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

if(__name__=="__main__"):
    Server()