from machine import Pin, ADC
from machine import UART


class PlantMonitor:

    wetness = 0
    temp = 0
    humidity = 0

    uart = None
    led_on = True

    # analog = ADC(28)

    def __init__(self):
        try:
            self.uart = UART(0, 9600, timeout=400)
        except:
            raise Exception("UART not available")
    
    def get_wetness(self):
        return float(self.request_property("w"))
    
    def get_temp(self):
        return float(self.request_property("t"))
    
    def get_humidity(self):
        return float(self.request_property("h"))
    
    def led_off(self):
        self.uart.write("l0")

    def led_on(self):
        self.uart.write("l1")

    def request_property(self, cmd):
        self.uart.write(cmd)
        line = self.uart.readline()
        if line != None and len(line) > 3:
            value_str = line[2:-2].decode()
            return value_str
        else:
            print('Communication Problem with Plant Monitor. Check your wiring.')
            return 0