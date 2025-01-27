from machine import Pin
from MOTOR import Motor

class Bot:
    def __init__(self):
        self.L_motor = Motor(1)  # Left Motor
        self.R_motor = Motor(2)  # Right Motor
        self.sensor_left = Pin(3, Pin.IN)  # Left sensor
        self.sensor_middle = Pin(4, Pin.IN) # middle sensor
        self.sensor_right = Pin(5, Pin.IN)  # Right sensor
        self.running = True  

    def update_sensors(self):
        self.s_lineL = self.sensor_left.value()  # 0=BLACK 1=WHITE
        self.s_lineM = self.sensor_middle.value()  
        self.s_lineR = self.sensor_right.value()  

    def bank_L(self):
        # Turn Left
        self.L_motor.Forward(80)
        self.R_motor.Forward(100)

    def bank_R(self):
        # Turn Right
        self.L_motor.Forward(100)
        self.R_motor.Forward(80)

    def forward(self):
        self.L_motor.Forward(80)
        self.R_motor.Forward(80)

    def line_following_onoff(self):
        self.update_sensors()
        if self.s_lineL == 0 and self.s_lineM == 1 and self.s_lineR == 0:  
            self.forward()
        elif self.s_lineL == 1 and self.s_lineM == 1 and self.s_lineR == 0:  
            self.bank_L()
        elif self.s_lineL == 0 and self.s_lineM == 1 and self.s_lineR == 1:
            self.bank_R()

    def run(self):
        try:
            while self.running:
                self.line_following_onoff()
        except KeyboardInterrupt:
            print("Stopping the bot...")
            self.running = False
