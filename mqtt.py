import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe("meena")

def on_message(client, userdata, msg):
    mpu_data = eval(msg.payload)
    print(mpu_data['Ax'],mpu_data['Ay'],mpu_data['Az'],mpu_data['Gx'],mpu_data['Gy'],mpu_data['Gz'])

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

broker = "broker.mqtt-dashboard.com"
client.connect(broker,1883,60)
client.loop_forever()

