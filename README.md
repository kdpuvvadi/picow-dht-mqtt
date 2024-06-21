# picow-dht-mqtt

rpi Pico W weather station with DHT and publish on mqtt

## config

```python
wifi_ssid = 'ssid'
wifi_password = 'wifi_password'
mqtt_server = b'10.20.20.20' # mqtt broker address without port
mqtt_username = b'username' # mqtt user username
mqtt_password = b'password' # mqtt user password
```

## mqtt Home Assistant autodiscovery

Topic: `homeassistant/sensor/kitchenthermo/config`

Payload

```json
{
  "object_id": "thermo_kitchen_temparature",
  "unique_id": "thermo_kitchen_temparature",
  "name": "Kitchen Temparature",
  "state_topic": "home/kitchen/climate",
  "value_template": "{{ value_json.Temparature }}"
}
```

## Multi Entity autodiscovery

### Entity 1

Topic: `homeassistant/sensor/kitchenthermo/temparature/config`

Payload:

```json
{
  "device": {
    "identifiers": "thermo_kitchen",
    "manufacturer": "Example Inc",
    "model": "PicoW",
    "name": "PicoW Thermostat"
  },
  "object_id": "thermo_kitchen_temparature",
  "unique_id": "thermo_kitchen_temparature",
  "name": "Kitchen Temparature",
  "state_topic": "home/kitchen/climate",
  "value_template": "{{ value_json.Temparature }}",
  "device_class": "temperature"
}
```

### Entity 2

Topic: `homeassistant/sensor/kitchenthermo/humidity/config`

Payload:

```json
{
  "device": {
    "identifiers": "thermo_kitchen",
    "manufacturer": "Puvvadi",
    "model": "PicoW",
    "name": "PicoW Thermostat"
  },
  "object_id": "thermo_kitchen_humidity",
  "unique_id": "thermo_kitchen_humidity",
  "name": "Kitchen Humidity",
  "state_topic": "home/kitchen/climate",
  "value_template": "{{ value_json.Humidity }}",
  "device_class": "humidity"
}
```

### Entity 3

Topic: `homeassistant/sensor/kitchenthermo/ip/config`

Payload:

```json
{
  "device": {
    "identifiers": "thermo_bedroom",
    "manufacturer": "Puvvadi",
    "model": "PicoW",
    "name": "Bedroom Thermostat"
  },
  "object_id": "thermo_bedroom_ip",
  "unique_id": "thermo_bedroom_ip",
  "name": "IP",
  "state_topic": "home/bedroom/climate",
  "value_template": "{{ value_json.IP }}"
}
```
