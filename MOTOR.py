from machine import Pin, PWM
from utime import sleep

class Motor:
    
    def __init__(self):
        self.m1Dir = Pin(7 , Pin.OUT) # set motor direction
        self.pwm1 = PWM(Pin(6)) # set speed
        self.pwm1.freq(1000) # set max frequency
        self.pwm1.duty_u16(0) # set duty cycle
 
    def off(self):
        self.pwm1.duty_u16(0)
        
    def Forward(self, speed): # speed range 0-100
        self.m1Dir.value(0)
        self.pwm1.duty_u16(int(65535*speed/100))
        
    def Reverse(self, speed): # speed range 0-100
        self.m1Dir.value(1)
        self.pwm1.duty_u16(int(65535*speed/100))
        
        

        