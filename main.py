# coding=utf-8
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import rpyc
from rpyc.utils.server import ThreadedServer # or ForkingServer

class MyService(rpyc.Service):
    get_module = ""
    #
    # ... you service's implementation
    #
    pass

def main():
    server = ThreadedServer(MyService, port=12345, protocol_config = {"allow_public_attrs" : True})
    server.start()

if __name__ == "__main__":
    server = ThreadedServer(MyService, port = 12345)
    server.start()

"""
https://wiki.mchobby.be/index.php?title=FEATHER-CHARGER-FICHIER-MICROPYTHON
ampy -p COM4 put client.py /CameraMatcher/client.py

import sys
sys.path.append("/CameraMatcher")
from CameraMatcher.client import Kernel
k = Kernel()
k.main()

"""
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
