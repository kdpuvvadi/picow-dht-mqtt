from time import sleep
from umqtt.simple import MQTTClient
import config
from phew import connect_to_wifi
import dht
import machine
from machine import Pin
import json

ip = connect_to_wifi(config.wifi_ssid, config.wifi_password)
print("connected to IP ", ip)

MQTT_TOPIC = 'home/bedroom/climate'

sensor = dht.DHT11(Pin(3))

MQTT_SERVER = config.mqtt_server
MQTT_PORT = 1883
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b'bedroom climate'
MQTT_KEEPALIVE = 7200
MQTT_SSL = False
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

class Thermostat:
    def __init__(
        self,
        identifiers,
        manufacturer,
        model,
        device_name,
        object_id,
        unique_id,
        name,
        state_topic,
        value_template,
        device_class,
        unit_of_measurement,
    ):
        self.init_device(identifiers, manufacturer, model, device_name)
        self.object_id = object_id
        self.unique_id = unique_id
        self.name = name
        self.state_topic = state_topic
        self.value_template = value_template
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement

    def init_device(self, identifiers, manufacturer, model, device_name):
        self.device_identifiers = identifiers
        self.device_manufacturer = manufacturer
        self.device_model = model
        self.device_name = device_name

    def to_dict(self):
        return {
            "device": {
                "identifiers": self.device_identifiers,
                "manufacturer": self.device_manufacturer,
                "model": self.device_model,
                "name": self.device_name,
            },
            "object_id": self.object_id,
            "unique_id": self.unique_id,
            "name": self.name,
            "state_topic": self.state_topic,
            "value_template": self.value_template,
            "device_class": self.device_class,
            "unit_of_measurement": self.unit_of_measurement,
        }

    def to_json(self):
        return json.dumps(self.to_dict()).encode('utf-8')

entity_temparature = Thermostat(
    identifiers="thermo_kitchen",
    manufacturer="Puvvadi",
    model="PicoW",
    device_name="PicoW Thermostat",
    object_id="thermo_kitchen_temparature",
    unique_id="thermo_kitchen_temparature",
    name="Kitchen Temparature",
    state_topic="home/kitchen/climate",
    value_template="{{ value_json.Temparature }}",
    device_class="temperature",
    unit_of_measurement= chr(176) + "C",
)

entity_humidity = Thermostat(
    identifiers="thermo_kitchen",
    manufacturer="Puvvadi",
    model="PicoW",
    device_name="PicoW Thermostat",
    object_id="thermo_kitchen_humidity",
    unique_id="thermo_kitchen_humidity",
    name="Kitchen Humidity",
    state_topic="home/kitchen/climate",
    value_template="{{ value_json.Humidity }}",
    device_class="humidity",
    unit_of_measurement= "%",
)

entity_ip = Thermostat(
    identifiers="thermo_kitchen",
    manufacturer="Puvvadi",
    model="PicoW",
    device_name="PicoW Thermostat",
    object_id="thermo_kitchen_ip",
    unique_id="thermo_kitchen_ip",
    name="Kitchen Thermostat IP",
    state_topic="home/kitchen/climate",
    value_template="{{ value_json.ip }}",
    device_class="",
    unit_of_measurement="",
)

MQTT_AUTODISC_TEMP = entity_temparature.to_json()
MQTT_AUTODISC_TEMP_TOPIC = 'homeassistant/sensor/bedroomthermo/temparature/config'

MQTT_AUTODISC_HUM = entity_humidity.to_json()
MQTT_AUTODISC_HUM_TOPIC = 'homeassistant/sensor/bedroomthermo/humidity/config'

MQTT_AUTODISC_IP = entity_ip.to_json()
MQTT_AUTODISC_IP_TOPIC = 'homeassistant/sensor/bedroomthermo/ip/config'

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

def auto_discovery():
    publish_mqtt(MQTT_AUTODISC_IP_TOPIC, MQTT_AUTODISC_IP)
    sleep(1)
    publish_mqtt(MQTT_AUTODISC_TEMP_TOPIC, MQTT_AUTODISC_TEMP)
    sleep(1)
    publish_mqtt(MQTT_AUTODISC_HUM_TOPIC, MQTT_AUTODISC_HUM)
    sleep(1)

try:
    client = connect_mqtt()
    auto_discovery()
    sleep(2)
    while True:
        sensor.measure()
        payload = json.dumps({ "Temperature": sensor.temperature(), "Humidity":  sensor.humidity(), "IP": ip})
        publish_mqtt(MQTT_TOPIC, str(payload))
        sleep(2)

except Exception as e:
    print('Error:', e)
    machine.reset()
