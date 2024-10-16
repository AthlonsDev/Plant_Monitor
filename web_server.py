import network
import socket
from time import sleep
#from picozero import pico_temp_sensor, pico_led
import machine

ssid = ""
password = ""

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan,isconnected() == False:
        print('Waiting for Connection')
        sleep(1)
    print(waln.ifconfig())
    
try:
    connect()
except KeyboardInterrupt:
    machine.reset()