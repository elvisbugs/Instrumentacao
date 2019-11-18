# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import font
import tkinter.scrolledtext as scrolledtext
from tkinter import ttk
import psutil
import subprocess
import os
import webPage as wp

class Window:
    def __init__(self, icon, title):
        #destroy any mqtt broker if exists
        self.stopBroker(True)

        self.meter = None
        self.proc = None

        self.window = Tk()
        self.window.title(title)
        self.window.resizable(0,0)

        self.window.iconbitmap(default=icon)

        #width and height window
        self.wdWidth = self.window.winfo_screenwidth()
        self.wdHeight = self.window.winfo_screenheight()

        self.bg = '#161719'
        self.font = 'Verdana 10 bold'

        self.window.configure(background=self.bg)

        self.setWindow()

        self.actualDir = os.getcwd() + "\\mosquitto\\mosquitto\\"
        
        #start a new mqtt broker
        self.runBroker()
    
    def getWindowSize(self):
        return self.wdWidth, self.wdHeight
       
    def browserFrame(self):
        url = 'http://localhost:3000/d/w4UNZzxZk/application?orgId=1&refresh=1s&kiosk'
        self.meter = wp.WebPage(self.window,'10;10','700;960',os.getcwd(),url)

    #decode position and size strings
    def decodePos(self,position):
        x = int(position.rsplit(";")[0])
        y = int(position.rsplit(";")[1])
        return x,y

    #define window size and centered
    def setWindow(self):
        self.widgetElements = dict()

        windowPosition = str(950) + "x" + str(690) #+ "+" + str(x_size//2) + "+" + str(y_size//2)
        self.window.geometry(windowPosition)
    
    #destroy the broker started with the object    
    def close(self):
        self.stopBroker(False)
        self.meter.close()
        del self.meter
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
                 bg = 'white',
                 fg = self.bg,
                 relief = SOLID,
                 font=(self.font))

        x, y = self.decodePos(position)
        btn.place(x=x, y=y)
        self.addElement(btn, txtBtn)
    
    def putSeparatorH(self,position):
        x,y = self.decodePos(position)
        separator = ttk.Separator(self.window, orient=HORIZONTAL)
        separator.place(x=x,y=y,relwidth=350)
    
    def putSeparatorV(self,position):
        x,y = self.decodePos(position)
        separator = ttk.Separator(self.window, orient=VERTICAL)
        separator.place(x=x,y=y,relheight=360)

    def addTxt(self, position, width, title,defaultTxt):
        x,y = self.decodePos(position)

        txt = Entry(self.window,
                relief=SOLID, 
                font = (self.font + ' italic'),
                bg='grey',
                fg='white',
                width=width,
                textvariable = StringVar()
                )
        
        txt.focus_set()
        txt.configure(insertbackground = 'white')

        txt.place(x=x,y=y)
        #clean txt
        txt.delete(0,END)
        #default value
        txt.insert(0, defaultTxt)      
        self.addElement(txt, title)
    
    def addLabel(self, position, name, defautlText):
        x,y = self.decodePos(position)

        label = Label(self.window, 
            text = defautlText, 
            bg = self.bg, 
            fg = 'white',
            font = self.font)

        label.place(x = x, y = y)
        self.addElement(label,name)

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

        for proc in psutil.process_iter():
            if proc.name() == procname1 or proc.name() == procname2:
                proc.kill()

    