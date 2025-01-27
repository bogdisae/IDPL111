from machine import Pin
from MOTOR import Motor
import time

class Bot:
    def __init__(self):
        self.R_motor = Motor(4, 5)  # Right Motor
        self.L_motor = Motor(7, 6)  # Left Motor
        self.sensor_left = Pin(10, Pin.IN)  # Left sensor
        self.sensor_middle = Pin(11, Pin.IN) # middle sensor
        self.sensor_right = Pin(12, Pin.IN)  # Right sensor
        self.running = True  

    def update_sensors(self):
        self.s_lineL = self.sensor_left.value()  # 0=BLACK 1=WHITE
        self.s_lineM = self.sensor_middle.value()  
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

    def follow_line(self):

        self.update_sensors()
        if self.s_lineL == 0 and self.s_lineM == 1 and self.s_lineR == 0:  
            self.forward()
        elif self.s_lineL == 1 and self.s_lineM == 1 and self.s_lineR == 0:  
            self.bank_L()
        elif self.s_lineL == 0 and self.s_lineM == 1 and self.s_lineR == 1:
            self.bank_R()
        elif self.s_lineL == 1 and self.s_lineM == 0 and self.s_lineR == 0:
            self.bank_L()
        elif self.s_lineL == 0 and self.s_lineM == 0 and self.s_lineR == 1:
            self.bank_R()

    def run(self):
        while self.running:
            self.follow_line()


