from machine import Pin, PWM
from utime import sleep
class Motor:
    def __init__(self, DIR, PinPWM):

        self.m1Dir = Pin(DIR , Pin.OUT) # set motor direction
        self.pwm1 = PWM(Pin(PinPWM)) # set speed
        self.pwm1.freq(1000) # set max frequency
        self.pwm1.duty_u16(0) # set duty cycle
    def off(self):
        self.pwm1.duty_u16(0)
    def Forward(self):
        self.m1Dir.value(0) # forward = 0 reverse = 1 motor 1
        self.pwm1.duty_u16(int(65535*100/100)) # speed range 0-100 motor 1
    def Reverse(self):
        self.m1Dir.value(1)
        self.pwm1.duty_u16(int(65535*30/100))


motor1 = Motor(7,6)
motor2 = Motor(4,5)

motor2.off()
motor1.Forward()
