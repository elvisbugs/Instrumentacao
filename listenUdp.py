# -*- coding: latin-1 -*-
from threading import Thread
from DbConnector import *
import socket

class UdpClient(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.objdb = DbConnector()
        UDP_IP = "192.168.1.101"
        UDP_PORT = 4242

        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
    
    def close(self):
        self.objdb.exit()
        del self.objdb

    #execute linstener async
    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.write(data.decode('utf-8'))
    
    #insert the received data on database
    def write(self,data):
        try:
           dblData = float(data)
           self.objdb.insert(dblData)
        except EOFError:
           pass
        