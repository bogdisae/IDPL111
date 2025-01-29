from machine import Pin, PWM
import time

# Servo parameters
max_duty = 7864
min_duty = 1802
half_duty = int(max_duty / 2)

class Servo:
    def __init__(self, pin=15):
        self.pwm = PWM(Pin(pin)) 
        self.pwm.freq(50)  # Standard servo frequency
        self.pwm.duty_u16(min_duty)  # Initial position at 0 degrees

    def off(self):  # Servo at 0 degrees
        self.pwm.duty_u16(min_duty)
        
    def half(self):  # Servo at 90 degrees
        self.pwm.duty_u16(half_duty)
        
    def full(self):  # Servo at 180 degrees
        self.pwm.duty_u16(max_duty)

def activate_servo(): #mechanism of lifting objects
    servo = Servo()  
    servo.full()  # Move servo to 180 degrees
    time.sleep(1)  # Hold for 1 second
    servo.off()  # Move servo back to 0 degrees
