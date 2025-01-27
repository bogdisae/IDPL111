from machine import Pin, PWM
from utime import sleep

class Motor:
    
    def __init__(self, PinDIR, PinPWM):
            
        self.Dir = Pin(PinDIR , Pin.OUT) # set motor direction
        self.pwm = PWM(Pin(PinPWM)) # set speed
        self.pwm.freq(1000) # set max frequency
        self.pwm.duty_u16(0) # set duty cycle
        print(f'motor {PinDIR}, {PinPWM} connected')
 
    def off(self):
        self.pwm.duty_u16(0)
        
    def Forward(self, speed): # speed range 0-100
        self.Dir.value(0)
        self.pwm.duty_u16(int(65535*speed/100))
        
    def Reverse(self, speed): # speed range 0-100
        self.Dir.value(1)
        self.pwm.duty_u16(int(65535*speed/100))
        

        
