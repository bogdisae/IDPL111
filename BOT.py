from machine import Pin, PWM
from MOTOR import Motor
import time

class Bot:
    def __init__(self):
        
        # MOTORS:
        self.R_motor = Motor(4, 5)  # Right Motor
        self.L_motor = Motor(7, 6)  # Left Motor
        
        # SENSORS
        self.sensor_left = Pin(10, Pin.IN)  # Left (off the line) sensor
        self.sensor_middle_left = Pin(11, Pin.IN) # Middle left (on the line) sensor
        self.sensor_middle_right = Pin(12, Pin.IN) # Middle right (on the line) sensor
        self.sensor_right = Pin(13, Pin.IN)  # Right (off the line) sensor
        
        # TURNING
        self.turning = False
        self.turn_time = 0 
        
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
            
    def turn(self):
        direction = "L" # this has been included for testing. In the future this will be retrieved from a navigation module
        
        # allow time for centre of turning of bot to reach junction (need to experimentally tune this time)
        if time.time() - self.turn_time < 1:
            self.follow_line()
        
        # turn the bot
        else: 
            if direction == "L":
                self.L_motor.Reverse(50)
                self.R_motor.Forward(50)
            
            elif direction == "R":
                self.L_motor.Forward(50)
                self.R_motor.Reverse(50)
        
        # stop turning when middle sensor reads the line again (needs adjusting to make sure the correct sensor is used)
        if (time.time() - self.turn_time > 1.5) and (self.s_lineML == 1):
            self.turning = False
            
            
    def follow_line(self):
        
        if self.s_lineML == 1 and self.s_lineMR == 1: #on the line 
            self.forward()
        elif self.s_lineML == 1 and self.s_lineMR == 0: #too right 
            self.bank_L()
        elif self.s_lineML == 0 and self.s_lineMR == 1: #too left
            self.bank_R()
        else: #off the line
            pass
        
    def drive(self):
        
        self.update_sensors()
        
        if not self.turning:
            self.follow_line()
        
        # if the far left/right sensors detect a junction, trigger turning sequence
        if (self.s_lineL == 1 or self.s_lineR == 1) and not self.turning:
                self.turn_time = time.time()
                self.turning = True
                
        if self.turning:
                self.turn()
        
    def run(self):
        while self.running:
            self.drive()
                





