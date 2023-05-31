import time

from api import TaskApi
import random
import json

client_id = f'hir-alg-mqtt-{random.randint(0, 1000)}'
tapi = TaskApi('http://192.168.0.209', 1883, 'admin', 'mx123456', client_id)
# tapi = TaskApi('broker.hivemq.com', 1883, 'admin', 'mx123456', client_id)

mqtt_cli = tapi.connect_mqtt()

result = {
    'count': 100,
    'class': 'normal crowd'
}

tapi.update_task('infer_demo', json.dumps(result))
