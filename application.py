# -*- coding: UTF-8 -*-
import window as wd
import listenMQTT as mqtt
import serial
import time

def grafanaBtn():
    pass

def applyOnEsp():
    pass
    
#start a new window with ico passed     
window = wd.Window("dbIcon.ico", "Medidor de Nível de pressão sonora")

# s = serial.Serial('COM1')

window.addBtn("700;500", "Open Grafana", grafanaBtn)
window.addBtn("500;100", "Apply WiFi Configs", applyOnEsp)

# window.NormalLabel("")

# subscriber = mqtt.MqttClient(window.getElement('TxtMqttSub'))
# subscriber.start()

#window.browserFrame("soundMenter")

#window.addFrame('5;5','360;360','frame')

window.exec()
window.close()

#del subscriber