# -*- coding: latin-1 -*-
import window as wd

def grafanaBtn():
    pass
    
window = wd.Window("dbIcon.ico")

btnBroker = "Start Broker"

window.addBtn("5x5", btnBroker, grafanaBtn)

window.exec()
window.close()