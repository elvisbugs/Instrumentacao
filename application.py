# -*- coding: UTF-8 -*-
import window as wd
import serial

def grafanaBtn():
    pass

def applyOnEsp():
    pass
    
#start a new window with ico passed     
window = wd.Window("dbIcon.ico", "Medidor de Nível de pressão sonora")

#s = serial.Serial('COM1')

window.addBtn("700;500", "Open Grafana", grafanaBtn)
window.addBtn("5;100", "Apply WiFi Configs", applyOnEsp)
window.addTxt("7;5","Title")

window.exec()
window.close()