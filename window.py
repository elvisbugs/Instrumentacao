# -*- coding: latin-1 -*-
from tkinter import *
import psutil
import subprocess
import os

class Window:
    def __init__(self, icon):
        self.window = Tk()
        self.window.iconbitmap(default=icon)
        self.setWindow()
        self.actualDir = os.getcwd() + "\\mosquitto\\mosquitto\\"
        self.runBroker()

    def setWindow(self):
        self.widgetElements = dict()
        self.x_size = self.window.winfo_screenwidth() // 2
        self.y_size = self.window.winfo_screenheight() // 2

        windowPosition = str(self.x_size) + "x" + str(self.y_size) + "+" + str(self.x_size//2) + "+" + str(self.y_size//2)
        self.window.geometry(windowPosition)
    def close(self):
        self.stopBroker()

    def exec(self):
        self.window.mainloop()

    def getWindow(self):
        return self.window

    def addBtn(self, pos, txtBtn, callback):
        btn = Button(self.window, text = txtBtn, command = callback)
        xy = pos.rsplit("x")
        btn.place(x=int(xy[0]),y=int(xy[1]))
        self.widgetElements[txtBtn] = btn

    def getElement(self, element):
        if element in self.widgetElements:
            return self.widgetElements.get(element)
        else:
            raise Exception("O elemento " + element + " não foi adicionado!")
    
    def runBroker(self):
        command = ["cd", self.actualDir, "&", "mosquitto", "-v"]
        subprocess.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    
    def stopBroker(self):
        procname = "mosquitto.exe"
        for proc in psutil.process_iter():
            if proc.name() == procname:
                proc.kill()