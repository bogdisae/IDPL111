from machine import Pin

class Light:
    def __init__(self):
        self.led = Pin(28, Pin.OUT)
    
    def on(self):
        self.led.value(1)
    
    def off(self):
        self.led.value(0)
