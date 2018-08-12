import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe("meena")

def on_message(client, userdata, msg):
    print(msg.topic +" "+str(msg.payload))

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

broker = "broker.mqtt-dashboard.com"
client.connect(broker,1883,60)
client.loop_forever()
    
