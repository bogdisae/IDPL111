from machine import Pin, PWM
from utime import sleep

class Motor:
    
    def __init__(self, motor_no):
        
        if motor_no == 1:
            Dir_pin = 7
            PWM_pin = 6
            
        elif motor_no == 2:
            Dir_pin = 3
            PWM_pin = 2
            
        self.Dir = Pin(Dir_pin , Pin.OUT) # set motor direction
        self.pwm = PWM(Pin(PWM_pin)) # set speed
        self.pwm.freq(1000) # set max frequency
        self.pwm.duty_u16(0) # set duty cycle
 
    def off(self):
        self.pwm.duty_u16(0)
        
    def Forward(self, speed): # speed range 0-100
        self.Dir.value(0)
        self.pwm.duty_u16(int(65535*speed/100))
        
    def Reverse(self, speed): # speed range 0-100
        self.Dir.value(1)
        self.pwm.duty_u16(int(65535*speed/100))
        
        

        