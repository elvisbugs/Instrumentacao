# -*- coding: latin-1 -*-
from tkinter import *
import subprocess
from threading import Thread 
import paho.mqtt.client as mqtt 
import window as wd

#brokerStartBtn = Button(window)
#brokerStartBtn.pack()

window = wd.Window()
window.exec()

class Broker(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        p = subprocess.Popen("mosquitto -v", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()        

#objBroker = Broker()
#objBroker.start()

