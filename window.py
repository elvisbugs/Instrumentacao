# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import font
import tkinter.scrolledtext as scrolledtext
import psutil
import subprocess
import os
import webPage as wp

class Window:
    def __init__(self, icon, title):
        #destroy any mqtt broker if exists
        self.stopBroker(True)
        self.proc = None
        self.window = Tk()
        self.window.title(title)
        self.window.iconbitmap(default=icon)
        self.bg = '#161719'
        self.window.configure(background=self.bg)
        self.setWindow()
        self.actualDir = os.getcwd() + "\\mosquitto\\mosquitto\\"
        self.font = 'Verdana 10 bold'
        #start a new mqtt broker
        self.runBroker()
        url = 'http://localhost:3000/d/Y_l0I91Zz/db?orgId=1&kiosk'
        self.wp = wp.WebPage(self.window,'5;5','350;350',os.getcwd(),url)

    #define window size and centered
    def setWindow(self):
        self.widgetElements = dict()
        x_size = self.window.winfo_screenwidth() // 2
        y_size = self.window.winfo_screenheight() // 2

        windowPosition = str(x_size) + "x" + str(y_size) + "+" + str(x_size//2) + "+" + str(y_size//2)
        self.window.geometry(windowPosition)
    
    #destroy the broker started with the object    
    def close(self):
        self.stopBroker(False)
        del self.wp
        del self.window

    #run the window
    def exec(self):
        self.window.mainloop()

    #return the current window instance
    def getWindow(self):
        return self.window

    #add a btn on current window
    def addBtn(self, position, txtBtn, callback):
        btn = Button(self.window,
                 text = txtBtn, command = callback, 
                 bg = self.bg,
                 fg = 'white',
                 relief = RAISED,
                 font=(self.font))

        x = int(position.rsplit(";")[0])
        y = int(position.rsplit(";")[1])
        btn.place(x=x, y=y)
        self.addElement(btn, txtBtn)

    def addTxt(self, position, title, size):
        height = int(size.rsplit(";")[0])
        width = int(size.rsplit(";")[1])
        x = int(position.rsplit(";")[0])
        y = int(position.rsplit(";")[1])

        #txt = scrolledtext.ScrolledText(self.window, height=height, width=width, font = (self.font))
        frame = Frame(self.window)
        frame.place(x=x, y=y)
        #txt.insert(END, "")
        self.addElement(frame, title)
    
    def addLabel(self, position, name, defautlText):
        x = int(position.rsplit(";")[0])
        y = int(position.rsplit(";")[1])

        label = Label(self.window, 
            text = defautlText, 
            bg = self.bg, 
            fg = 'green',
            font = ('Verdana 50 bold'))

        label.place(x = x, y = y)
        self.addElement(label,name)

    def addFrame(self, position, size, name):
        x = int(position.rsplit(";")[0])
        y = int(position.rsplit(";")[1])
        h = int(size.rsplit(";")[0])
        w = int(size.rsplit(";")[1])

        frame = Frame(self.window, bg = self.bg, height = h, width = h)

        browser = BrowserFrame(frame,position, size, name)

        browser.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        frame.place(x = x, y = y)
        
        self.addElement(frame,name)

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
        self.proc = subprocess.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    
    #kill any process running a mqtt broker
    def stopBroker(self,starting):
        if not starting:
            self.proc.kill()
        procname1 = 'mosquitto.exe'
        procname2 = 'subprocess.exe'
        for proc in psutil.process_iter():
            if proc.name() == procname1 or proc.name() == procname2:
                proc.kill()