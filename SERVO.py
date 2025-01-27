from machine import Pin, PWM
from time import sleep

# Set Duty Cycle for Different Angles
max_duty = 7864
min_duty = 1802
half_duty = int(max_duty/2)

class Servo:
    
    def __init__(self):
        self.Dir = Pin(Dir_pin , Pin.OUT) # set motor direction
        self.pwm = PWM(Pin(15)) # set speed
        self.pwm.freq(50) # set max frequency
        self.pwm.duty_u16(1802)
        
    def off(self): #Servo at 0 degrees
        self.pwm.duty_u16(1802)
        
    def half (self): #Servo at 90 degrees
        self.pwm.duty_u16 (int(7864))
        
    def full (self, speed): #Servo at 180 degrees
        self.pwm.duty_u16 (7864)
        
    
             

