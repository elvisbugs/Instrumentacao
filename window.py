# -*- coding: latin-1 -*-
from tkinter import *
class Window:
    def __init__(self):
        self.window = Tk()
        self.setWindow()

    def __init__(self, icon):
        self.window = Tk()
        self.window.iconbitmap(default=icon)
        self.setWindow()

    def setWindow(self):
        self.widgetElements = dict()
        self.x_size = self.window.winfo_screenwidth() // 2
        self.y_size = self.window.winfo_screenheight() // 2

        windowPosition = str(self.x_size) + "x" + str(self.y_size) + "+" + str(self.x_size//2) + "+" + str(self.y_size//2)
        self.window.geometry(windowPosition)

    def exec(self):
        self.window.mainloop()

    def getWindow(self):
        return self.window

    def addBtn(self, pos, txtBtn, callback):
        btn = Button(self.window, text = txtBtn, command = callback)
        btn.pack()
        self.widgetElements[txtBtn] = btn

    def getElement(self, element):
        if element in self.widgetElements:
            return self.widgetElements.get(element)
        else:
            raise Exception("O elemento " + element + " não foi adicionado!")