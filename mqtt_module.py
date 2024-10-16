import network
import socket
from time import sleep
import json
import machine
import ssl
import constants
from umqtt.simple import MQTTClient
import ubinascii

ssid = "VM3412687"
password = "m8fvGjsJcfxz"
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())

def connect_internet():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    try:
        wlan.connect(ssid, password)
        while wlan.isconnected() == False:
            print('Waiting for Connection')
            sleep(1)
        print(wlan.ifconfig()) 
    except KeyboardInterrupt:
        machine.reset()

connect_internet()

def read_pem(file):
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)

key = read_pem(constants.CLIENT_KEY)
cert = read_pem(constants.CLIENT_CERT)
ca = read_pem(constants.AWS_BROKER_CA)
ssl_params = {"key": key,
        "cert": cert,
        "server_side": False,
        "cert_reqs": ssl.CERT_REQUIRED,
        "cadata": ca}

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED

mqtt_client = MQTTClient(
    # client_id=MQTT_CLIENT_ID,
    # server=constants.CORE_ENDPOINT,
    # ssl=ssl,
    # port=constants.port,
    # ssl_params=ssl_params,
        client_id=MQTT_CLIENT_ID,
        server=constants.CORE_ENDPOINT,
        port=constants.port,
        keepalive=7200,
        ssl=context
)

def connect():
    print("Connecting to AWS IoT Core")
    try:
        mqtt_client.connect()
        print("Connected to AWS IoT Core")
    except OSError as e:
        print("Error: ", e)
        sleep(1)
        machine.reset()

connect()

def publish_sensor_data(data):
    payload = {
        "point_number": 'temperature',
        "value": str(data),
        "topic": "Plant_Monitor/d"
    }
    mqtt_client.publish('Plant_Monitor/d', json.dumps(payload), client)