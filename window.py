# -*- coding: latin-1 -*-
from tkinter import *
import psutil
import subprocess
import os

class Window:
    def __init__(self, icon, title):
        #destroy any mqtt broker if exists
        self.stopBroker()
        self.window = Tk()
        self.window.title(title)
        self.window.iconbitmap(default=icon)
        self.setWindow()
        self.actualDir = os.getcwd() + "\\mosquitto\\mosquitto\\"
        #start a new mqtt broker
        self.runBroker()

    #define window size and centered
    def setWindow(self):
        self.widgetElements = dict()
        self.x_size = self.window.winfo_screenwidth() // 2
        self.y_size = self.window.winfo_screenheight() // 2

        windowPosition = str(self.x_size) + "x" + str(self.y_size) + "+" + str(self.x_size//2) + "+" + str(self.y_size//2)
        self.window.geometry(windowPosition)
    
    #destroy the broker started with the object    
    def close(self):
        self.stopBroker()

    #run the window
    def exec(self):
        self.window.mainloop()

    #return the current window instance
    def getWindow(self):
        return self.window

    #add a btn on current window
    def addBtn(self, position, txtBtn, callback):
        btn = Button(self.window, text = txtBtn, command = callback)
        xy = position.rsplit(";")
        btn.place(x=int(xy[0]),y=int(xy[1]))
        self.addElement(btn, txtBtn)

    def addTxt(self, position, title):
        txt = Text(self.window, height=2, width=30)
        txt.pack()
        txt.insert(END, "Just a text Widget\nin two lines\n")
        self.addElement(txt, title)
        #lt_text.pack()
    
    #add element to window
    def addElement(self, element, name):
        self.widgetElements[name] = element

    #return a specific element from window
    def getElement(self, element):
        if element in self.widgetElements:
            return self.widgetElements.get(element)
        else:
            raise Exception("O elemento " + element + " não foi adicionado!")
    
    #start the mqtt broker on localhost, 1883 port 
    def runBroker(self):
        command = ["cd", self.actualDir, "&", "mosquitto", "-v"]
        subprocess.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    
    #kill any process running a mqtt broker
    def stopBroker(self):
        procname = "mosquitto.exe"
        for proc in psutil.process_iter():
            if proc.name() == procname:
                proc.kill()