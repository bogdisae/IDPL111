from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin=13):
        # Servo parameters
        self.max_duty = 7864
        self.min_duty = 1802
        self.half_duty = int(self.max_duty / 2)

        self.pwm = PWM(Pin(pin)) 
        self.pwm.freq(50)  # Standard servo frequency
        self.pwm.duty_u16(self.min_duty)  # Initial position at 0 degrees


    def turn_to_angle(self, angle): # between 0 - 180 degrees
        self.pwm.duty_u16(int(angle * (self.max_duty - self.min_duty)/180) + self.min_duty)
        

