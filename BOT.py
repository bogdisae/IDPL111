from machine import Pin
from MOTOR import Motor
import time

class Bot:
    def __init__(self):
        self.R_motor = Motor(4, 5)  # Right Motor
        self.L_motor = Motor(7, 6)  # Left Motor
        self.sensor_left = Pin(10, Pin.IN)  # Left (off the line) sensor
        self.sensor_middle_left = Pin(11, Pin.IN) # Middle left (on the line) sensor
        self.sensor_middle_right = Pin(11, Pin.IN) # Middle right (on the line) sensor
        self.sensor_right = Pin(12, Pin.IN)  # Right (off the line) sensor
        self.running = True  

    def update_sensors(self):
        self.s_lineL = self.sensor_left.value()  # 0=BLACK 1=WHITE
        self.s_lineML = self.sensor_middle_left.value()
        self.s_lineMR = self.sensor_middle_right.value()  
        self.s_lineR = self.sensor_right.value()  

    def bank_L(self):
        # Turn Left
        self.L_motor.Forward(80)
        self.R_motor.Forward(100)
        time.sleep(0.5)

    def bank_R(self):
        # Turn Right
        self.L_motor.Forward(100)
        self.R_motor.Forward(80)
        time.sleep(0.5)

    def forward(self):
        self.L_motor.Forward(80)
        self.R_motor.Forward(80)
        time.sleep(0.5)
        
    def initiate_turning(self):            

    def follow_line(self):
        self.update_sensors()
        if self.s_lineL == 1 or self.s_lineR == 1: #
            initiate_turning()
        else:            
            if self.s_lineML == 1 and self.s_lineMR == 1: #on the line 
                self.forward()
            elif self.s_lineML == 1 and self.s_lineMR == 0: #too right 
                self.bank_L()
            elif self.s_lineML == 0 and self.s_lineMR == 1: #too left
                self.bank_R()
            else: #off the line
                pass
        
    def run(self):
        while self.running:
            self.follow_line()


