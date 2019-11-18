# -*- coding: UTF-8 -*-
import serial.tools.list_ports
from serial import Serial
from serial import SerialException
import time

class SerialCom:
    def __init__(self):
        ports = serial.tools.list_ports.comports()
        ports = sorted(ports)
        self.comList = []
        self.serDefault = None

        for port, desc, hwid in ports:
            self.comList.append(port + ' ' + desc)
            if(desc == 'USB-SERIAL CH340 (COM6)'):
                self.serDefault = port

    def write(self,message):
        ok = False
        while not ok:
            try:
                time.sleep(1)
                ser = Serial(self.serDefault,9600)
                bMessage = str.encode(message ,'ascii')
                ser.write(bMessage)
                ok = True
            except SerialException:
                pass

obj = SerialCom()
obj.write('#Elvis')
obj.write('*angaroth')
obj.write('@191.168.0.103')

