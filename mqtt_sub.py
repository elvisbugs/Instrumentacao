import subprocess

sub = 'mosquitto_sub -h localhost -p 1883 -t \"MNPS\"'

pub = 'mosquitto_pub -h localhost -p 1883 -t \"MNPS\" -m '

def startListen():
    subprocess.call(sub)

startListen()