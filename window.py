# -*- coding: latin-1 -*-
from tkinter import *
class Window:
    def __init__(self):
        self.window = Tk()
        self.x_size = self.window.winfo_screenwidth() // 2
        self.y_size = self.window.winfo_screenheight() // 2

        windowPosition = str(self.x_size) + "x" + str(self.y_size) + "+" + str(self.x_size//2) + "+" + str(self.y_size//2)
        print(windowPosition)
        self.window.geometry(windowPosition)

    def exec(self):
        self.window.mainloop()