from machine import Pin, PWM
from time import sleep
# Set up PWM Pin for servo control
servo_pin = machine.Pin(15)
servo = PWM(servo_pin)
# Set Duty Cycle for Different Angles
max_duty = 7864
min_duty = 1802
half_duty = int(max_duty/2)

class Servo:
    
    def __init__(self):
        self.Dir = Pin(Dir_pin , Pin.OUT) # set motor direction
        self.pwm = PWM(Pin(PWM_pin)) # set speed
        self.pwm.freq(50) # set max frequency
        # Set Duty Cycle for Different Angles
        self.pwm.max_duty = 7864
        self.pwm.min_duty = 1802
        self.pwm.half_duty = int(max_duty/2)

try:
    while True:
        #Servo at 0 degrees
        servo.duty_u16(min_duty)
        sleep(2)
        #Servo at 90 degrees
        servo.duty_u16(half_duty)
        sleep(2)
        #Servo at 180 degrees
        servo.duty_u16(max_duty)
        sleep(2)
except KeyboardInterrupt:
 print("Keyboard interrupt")
 # Turn off PWM
 servo.deinit()