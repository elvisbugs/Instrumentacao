# -*- coding: latin-1 -*-
from tkinter import *
from tkinter import messagebox
import subprocess
from threading import Thread 
import window as wd

serverState = False

class Broker(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        p = subprocess.Popen("mosquitto -v", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()  

def btnBrokerServer():
    global serverState
    if not serverState:
        objBroker.start()
        serverState = True
    else:
        objBroker.stop()
        serverState = False

objBroker = Broker()

window = wd.Window("dbIcon.ico")

btnBroker = "Start Broker"

window.addBtn(55, btnBroker, btnBrokerServer)

window.exec()
#objBroker = Broker()
#objBroker.start()

