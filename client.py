# https://micronote.tech/2020/07/I2C-Bus-with-a-NodeMCU-and-MicroPython/
from machine import Pin, I2C
import network
import socket
import time

class Kernel():

    def __init__(self):
        # global varsA
        self.ssid = "SFR_3088"#"Livebox-E8A6"  # "TP-LINK_B02DB9"
        self.mdp = "pryd3quimaxfaynjagjo"#"F24C5464A6C91C179CF2A41775"  # bmadekxcts8gmn2zbzlaayei6wf"
        self.target_ip = "192.168.1.25" #"192.168.1.38"  # wlan.ifconfig()[0]
        self.port = 10086

    def read_two_byte(self, idc_bus, chip_adr, reg_adr_1, reg_adr_2, bytes):
        # read the data from the register. These value are on two bytes:
        data_h = idc_bus.readfrom_mem(chip_adr, reg_adr_1, bytes)
        data_l = idc_bus.readfrom_mem(chip_adr, reg_adr_2, bytes)
        # combine the high and lox bytes
        data_h = data_h[0]
        data_l = data_l[0]
        # shifting hight byte to 8 places to the left
        data_h = data_h << 8
        # combine the high and low bytes
        data = data_h | data_l
        # handle negative value
        if data & 0b1000000000000000:
            data = -((data ^ 0b1111111111111111) + 1)
        return data


    def connect_to_access_point(self, ssid, mdp):
        # connect to access point
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, mdp)
        while (wlan.isconnected() == False):
            time.sleep(0.1)

    def init_socket(self):
        """define the socket of the client"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
        return sock

    def send_datas(self, datas):
        self.socket.sendto(datas, (self.target_ip, self.port))

    def main(self):
        ####################Accelerometre#######################
        i2c = I2C(scl=Pin(5), sda=Pin(4))  # i2c = Bus, scl = clock, sda = data
        # scaning for the adress device of the I2C bus, return adress of each slave (the composant attached to the main card)
        print(str(i2c.scan()))
        # set all the PWR_MGMT_1 to 0 to make sure the device is not in sleep mode
        i2c.writeto_mem(0x68, 0x6B, bytes([0]))
        while (True):
            lsbg = 16384.0  # lsb sensitvity number defined from the range table of the accelerometer
            accel_x = self.read_two_byte(i2c, 0x68, 0x3b, 0x3c, 1) / lsbg
            accel_y = self.read_two_byte(i2c, 0x68, 0x3d, 0x3e, 1) / lsbg
            accel_z = self.read_two_byte(i2c, 0x68, 0x3f, 0x40, 1) / lsbg
            # Gyro
            lsbds = 131.0  # degree per second sensitivity
            gyro_x = self.read_two_byte(i2c, 0x68, 0x43, 0x44, 1) / lsbds
            gyro_y = self.read_two_byte(i2c, 0x68, 0x45, 0x46, 1) / lsbds
            gyro_z = self.read_two_byte(i2c, 0x68, 0x47, 0x48, 1) / lsbds

            datas = str(accel_x)

            ##########WIFI###########
            # connect to access point
            self.connect_to_access_point(self.ssid, self.mdp)

            #########################

            #########Socket##############
            # open socket and send datas :
            self.socket = self.init_socket()
            self.send_datas(datas)
            #########################



if __name__ == "__main__":
    k=Kernel()
    k.main()
