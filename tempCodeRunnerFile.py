import subprocess
from threading import Thread 
import window as wd

class Broker(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        p = subprocess.Popen("mosquitto -v", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()  

def btnBrokerServer(serverState):
    if not serverState:
        objBroker.start()
        serverState = True
    else:
        print("Server false state")
        serverState = False

objBroker = Broker()

window = wd.Window("dbIcon.ico")

btnBroker = "Start Broker"
serverState = False
window.addBtn("5x5", btnBroker, btnBrokerServer(serverState))

window.exec()