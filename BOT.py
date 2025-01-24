from machine import Pin, PWM
from MOTOR import Motor

class Bot:
    
    def __init__(self):
    
        # Assign motors
        self.L_motor = Motor(1)
        self.R_motor = Motor(2)
    
        # Line sensors: 0 = black, 1 = white
        self.s_lineL = True #left
        self.s_lineR = False #right
        self.running = True
        
    def bank_L(self):
        self.L_motor.Forward(80)
        self.R_motor.Forward(100)
        
    def bank_R(self):
        self.L_motor.Forward(100)
        self.R_motor.Forward(80)
        
    def forward(self):
        self.L_motor.Forward(80)
        self.R_motor.Forward(80)
    
    def line_following_onoff(self):
        if (self.s_lineL and (not self.s_lineR)):
            self.bank_R()
        elif ((not self.s_lineL) and self.s_lineR):
            self.bank_L()
        else self.forward()
    
    def run(self):
        while(self.running):
            self.line_following_onoff()