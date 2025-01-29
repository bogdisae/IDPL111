from machine import Pin, PWM
from MOTOR import Motor
import time
from enum import Enum


# This is here for naming directions in the navigation to prevent bugs from miss-typing
class direct(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


PATHS = {
    "LA": [direct.RIGHT, direct.LEFT],  # Left warehouse to A
    "LB": [
        direct.STRAIGHT,
        direct.RIGHT,
        direct.STRAIGHT,
        direct.RIGHT,
    ],  # Left warehouse to B
    "LC": [
        direct.STRAIGHT,
        direct.RIGHT,
        direct.LEFT,
        direct.LEFT,
    ],  # Left warehouse to C
    "LD": [
        direct.STRAIGHT,
        direct.STRAIGHT,
        direct.RIGHT,
        direct.STRAIGHT,
        direct.RIGHT,
    ],  # Left warehouse to D
    "RA": [direct.LEFT, direct.STRAIGHT, direct.RIGHT],  # Right warehouse to A
    "RB": [direct.STRAIGHT, direct.LEFT, direct.LEFT],  # Right warehouse to B
    "RC": [
        direct.STRAIGHT,
        direct.LEFT,
        direct.STRAIGHT,
        direct.RIGHT,
        direct.LEFT,
    ],  # Right warehouse to C
    "RD": [
        direct.STRAIGHT,
        direct.STRAIGHT,
        direct.RIGHT,
        direct.LEFT,
    ],  # Right warehouse to D
    "AL": [direct.RIGHT, direct.LEFT],  # A to Left warehouse
    "BL": [
        direct.LEFT,
        direct.STRAIGHT,
        direct.LEFT,
        direct.STRAIGHT,
    ],  # B to Left warehouse
    "CL": [
        direct.RIGHT,
        direct.RIGHT,
        direct.LEFT,
        direct.STRAIGHT,
    ],  # C to Left warehouse
    "DL": [
        direct.LEFT,
        direct.STRAIGHT,
        direct.LEFT,
        direct.STRAIGHT,
        direct.STRAIGHT,
    ],  # D to Left warehouse
    "AR": [direct.LEFT, direct.STRAIGHT, direct.RIGHT],  # A to Right warehouse
    "BR": [direct.RIGHT, direct.RIGHT, direct.STRAIGHT],  # B to Right warehouse
    "CR": [
        direct.RIGHT,
        direct.LEFT,
        direct.STRAIGHT,
        direct.RIGHT,
        direct.STRAIGHT,
    ],  # C to Right warehouse
    "DR": [
        direct.RIGHT,
        direct.RIGHT,
        direct.STRAIGHT,
        direct.STRAIGHT,
    ],  # D to Right warehouse
    "HL": [direct.LEFT, direct.STRAIGHT, direct.LEFT],  # Home to Left warehouse
    "HR": [direct.RIGHT, direct.RIGHT],  # Home to Right warehouse
    "LH": [direct.RIGHT, direct.STRAIGHT, direct.RIGHT],  # Left warehouse to Home
    "RH": [direct.LEFT, direct.LEFT],  # Right warehouse to Home
}


class Bot:
    def __init__(self):
        
        # MOTORS:
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

    def bank(self, turning):  # anticlockwise positive
        self.L_motor.speed(self.speed - turning)
        self.R_motor.speed(self.speed + turning)

    def forward(self):
        self.L_motor.Forward(80)
        self.R_motor.Forward(80)
        time.sleep(0.5)
        
    def initiate_turning(self):            

    def follow_line(self):
        self.update_sensors()
        if self.s_lineL == 1 or self.s_lineR == 1:  #
            self.L_motor.speed(0)
            self.R_motor.speed(0)
            self.initiate_turning()
        elif self.s_lineML == 1 or self.s_lineMR == 1:
            self.proportional()
            self.integral()
            self.bank(self.turning_kp + self.turning_ki)
        else:
            # Off the line
            pass

    def run(self):
        while self.running:
            self.follow_line()


