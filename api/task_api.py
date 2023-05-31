import json
import paho.mqtt.client as mqtt_client

class TaskApi:
    def __init__(self, ip, port, username, password, client_id):
        self.status = 'disconnected'
        self.topic = '/hir/alg/crowd'
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client = None

    def connect_mqtt(self):
        if self.status == 'connected':
            return

        def on_publish(client, userdata, mid):
            print ("message published")

        # TODO: the on_connect callback not working
        def on_connect(client, userdata, flags, rc):
            print('on connect event')
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.status = 'connected'
            else:
                print("Failed to connect, return code %d\n", rc)
                self.status = 'disconnected'

        client_id = self.client_id
        self.client = mqtt_client.Client(client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.on_publish = on_publish
        self.client.connect(host=self.ip, port=self.port, keepalive=45)
        return self.client

    def update_task(self, task_id, result):

        params = {
            'task_id': task_id,
            'result': json.dumps(result)
        }
        f = json.dumps(params)
        print('publishing message')
        self.client.publish(self.topic, f)