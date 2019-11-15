# -*- coding: latin-1 -*-
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
   client.subscribe("MNPS/#")

# Callback responável por receber uma mensagem publicada no tópico acima
def on_message(client, userdata, msg):
    msg = str(msg.payload)
    print(msg.topic+" -  "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Seta um usuário e senha para o Broker, se não tem, não use esta linha
#client.username_pw_set("USUARIO", password="SENHA")
# Conecta no MQTT Broker
client.connect("127.0.0.1", 1883, 60)
# Inicia o loop
client.loop_forever()