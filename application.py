# -*- coding: UTF-8 -*-
import window as wd
import listenUdp as udp

import webbrowser

def grafanaBtn():
    webbrowser.open('http://localhost:3000/d/evJbqpTWk/application?orgId=1&refresh=1s&from=now-12h&to=now-2s', new=2)
    
#start a new window with ico passed
window = wd.Window("dbIcon.ico", "Sound Pressure Meter")
window.browserFrame()

window.addBtn("830;660", "Open Grafana", grafanaBtn)

listener = udp.UdpClient()
listener.start()

window.exec()
window.close()
listener.close()

del listener
del window