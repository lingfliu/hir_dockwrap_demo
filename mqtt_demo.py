# Import package
import paho.mqtt.client as mqtt
import random
import json

# Define Variables
MQTT_HOST = "192.168.0.209"
# MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "/hir/alg/crowd"
MQTT_MSG = json.dumps({
    'code': 'ok',
    'num': 12
})


# Define on_publish event function
def on_publish(client, userdata, mid):
	print ("Message Published...")

def on_connect(client, userdata, flags, rc):
    print('on connect event')
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


# Initiate MQTT Client
client_id = f'hir-alg-mqtt-{random.randint(0, 1000)}'
mqttc = mqtt.Client(client_id)

# Register publish callback function
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

# Connect with MQTT Broker
mqttc.username_pw_set("admin", "mx123456")
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Publish message to MQTT Broker
mqttc.publish(MQTT_TOPIC,MQTT_MSG)
# Disconnect from MQTT_Broker
mqttc.disconnect()