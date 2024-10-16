import machine
from machine import Pin, I2C
from monitor import PlantMonitor
import time
import uos
import json
import mqtt_module

pm = PlantMonitor()



while True:
    wetness = pm.get_wetness()
    temp = pm.get_temp()
    humidity = pm.get_humidity()
    
    # print("Wetness: {0} Temp: {1} Humidity: {2}".format(w, t, h))
    time.sleep(1)
    print(f'h:{humidity}. t:{temp}, w:{wetness}')

    mqtt_module.connect()
    
    