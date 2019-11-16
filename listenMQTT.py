# -*- coding: latin-1 -*-
import paho.mqtt.client as mqtt
from threading import Thread
from tkinter import *
import datetime

class MqttClient(Thread):
    def __init__(self,widget):
        Thread.__init__(self)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1", 1883, 60)
        self.message = ""
        self.widget = widget 
        
    def run(self):
        self.client.loop_forever()
    
    def write(self,msg):
        #crntTime = str(datetime.datetime.now().strftime('%H:%M:%S'))
        self.widget.config(text= msg + " dB")

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        self.client.subscribe("MNPS/#")

    # Callback responável por receber uma mensagem publicada no tópico acima
    def on_message(self, client, userdata, msg):
        msg = msg.payload
        strMsg = msg.decode()
        self.write(strMsg)
        