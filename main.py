from time import sleep
from umqtt.simple import MQTTClient
import config
from phew import connect_to_wifi
import dht
import machine
from machine import Pin
import json

MQTT_TOPIC = 'home/livingroom/climate'

sensor = dht.DHT11(Pin(3))

MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b'livingroom climate'
MQTT_KEEPALIVE = 7200
MQTT_SSL = False
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

ip = connect_to_wifi(config.wifi_ssid, config.wifi_password)
print("connected to IP ", ip)

def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise

def publish_mqtt(topic, value):
    client.publish(topic, value, retain=True)
    print(topic)
    print(value)
    print("Publish Done")

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  machine.reset()

try:
    client = connect_mqtt()
    while True:
        sensor.measure()
        payload = json.dumps({ "Temperature": sensor.temperature(), "Humidity":  sensor.humidity()})
        publish_mqtt(MQTT_TOPIC, str(payload))
        sleep(5)

except Exception as e:
    print('Error:', e)
    machine.reset()
