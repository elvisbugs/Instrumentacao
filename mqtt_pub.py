import os

sub = 'mosquitto_sub -h localhost -p 1883 -t \"MNPS\"'

pub = 'mosquitto_pub -h localhost -p 1883 -t "MNPS" -m '

def startMQTT():
    os.system('mosquitto -v')

for x in range(100):
    os.system(pub + '\"testando\"' + str(x))