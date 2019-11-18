# -*- coding: latin-1 -*-
import paho.mqtt.client as mqtt
from threading import Thread
from tkinter import *
import datetime
from DbConnector import *
from time import sleep
import ctypes

class MqttClient(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1", 1883, 60)
        self.objdb = DbConnector()
        self.before = datetime.datetime.now().time().strftime('%H:%M:%S')
    
    def close(self):
        self.objdb.exit()
        del self.objdb
        del self.client

    #execute linstener async
    def run(self):

        # user32 = ctypes.windll.user32

        # user32.keybd_event(0x12, 0, 0, 0) #Alt
        # sleep(0.01)
        # user32.keybd_event(0x09, 0, 0, 0) #Tab
        # sleep(0.01)
        # user32.keybd_event(0x09, 0, 2, 0) #~Tab
        # sleep(0.01)
        # user32.keybd_event(0x12, 0, 2, 0) #~Alt

        # user32.keybd_event(0x12, 0, 0, 0) #Alt
        # sleep(0.01)
        # user32.keybd_event(0x09, 0, 0, 0) #Tab
        # sleep(0.01)
        # user32.keybd_event(0x09, 0, 2, 0) #~Tab
        # sleep(0.01)
        # user32.keybd_event(0x12, 0, 2, 0) #~Alt

        
        self.client.loop_forever()
    
    #insert the received data on database
    def write(self,data):
        dblData = float(data)
        self.objdb.insert(dblData)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        self.client.subscribe("MNPS/#")

    # Callback responável por receber uma mensagem publicada no tópico acima
    def on_message(self, client, userdata, msg):
        FMT = '%H:%M:%S'
        now_ = datetime.datetime.now().time().strftime('%H:%M:%S')
        tdelta = datetime.datetime.strptime(now_, FMT) - datetime.datetime.strptime(self.before, FMT)
        if(tdelta.seconds > 1):
            self.before = now_
            msg = msg.payload
            strMsg = msg.decode()
            self.write(strMsg)
        