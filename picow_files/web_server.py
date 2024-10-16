import network
import socket
from time import sleep
#from picozero import pico_temp_sensor, pico_led
import machine
import ussl as tls
import constants
from umqtt.robust import MQTTClient

ssid = "VM3412687"
password = "m8fvGjsJcfxz"

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
    
def make_connections():
    # Connect to internet and set MPU to start taking readings
    connect_internet()
    return connectMQTT()



    
def connectMQTT():
    '''Connects to Broker'''
    context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
    context.verify_mode = tls.CERT_NONE
    # Client ID can be anything
    client = MQTTClient(
        client_id=b"admin",
        server="6823a25d60444b99b2c4359055e433db.s1.eu.hivemq.cloud",
        port=constants.port,
        user=constants.username,
        password= constants.password,
        keepalive=7200,
        ssl=context
    )
    client.connect()
    return client

def publish(topic, value, client):
    '''Sends data to the broker'''
    print(topic)
    print(value)
    client.publish(topic, value)
    print("Publish Done")

    

client = make_connections()

# while True:
#     publish('Topic', 'test _message', client)
#     sleep(1)