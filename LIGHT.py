from machine import Pin

class Light:
    def __init__(self):
        self.led = Pin(16, Pin.OUT)
    
    def on(self):
        led.value(1)
    
    def off(self):
        led.value(0)