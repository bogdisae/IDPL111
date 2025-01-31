from machine import Pin
from MOTOR import Motor
import time

PATHS = {
    "LA": ["right", "left"],  # Left warehouse to A
    "LB": [
        "straight",
        "right",
        "straight",
        "right",
    ],  # Left warehouse to B
    "LC": [
        "straight",
        "right",
        "left",
        "left",
    ],  # Left warehouse to C
    "LD": [
        "straight",
        "straight",
        "right",
        "straight",
        "right",
    ],  # Left warehouse to D
    "RA": ["left", "straight", "right"],  # Right warehouse to A
    "RB": ["straight", "left", "left"],  # Right warehouse to B
    "RC": [
        "straight",
        "left",
        "straight",
        "right",
        "left",
    ],  # Right warehouse to C
    "RD": [
        "straight",
        "straight",
        "right",
        "left",
    ],  # Right warehouse to D
    "AL": ["right", "left"],  # A to Left warehouse
    "BL": [
        "left",
        "straight",
        "left",
        "straight",
    ],  # B to Left warehouse
    "CL": [
        "right",
        "right",
        "left",
        "straight",
    ],  # C to Left warehouse
    "DL": [
        "left",
        "straight",
        "left",
        "straight",
        "straight",
    ],  # D to Left warehouse
    "AR": ["left", "straight", "right"],  # A to Right warehouse
    "BR": ["right", "right", "straight"],  # B to Right warehouse
    "CR": [
        "right",
        "left",
        "straight",
        "right",
        "straight",
    ],  # C to Right warehouse
    "DR": [
        "right",
        "right",
        "straight",
        "straight",
    ],  # D to Right warehouse
    "HL": ["left", "straight", "left"],  # Home to Left warehouse
    "HR": ["right", "right"],  # Home to Right warehouse
    "LH": ["right", "straight", "right"],  # Left warehouse to Home
    "RH": ["left", "left"],  # Right warehouse to Home
}

class Light:
    def __init__(self):
        self.led = Pin(16, Pin.OUT)
    
    def on(self):
        led.value(1)
    
    def off(self):
        led.value(0)
    
class Bot:
    def __init__(self):
        
        # MOTORS
        self.R_motor = Motor(4, 5)  # Right Motor
        self.L_motor = Motor(7, 6)  # Left Motor

        # SENSORS
        self.sensor_left = Pin(11, Pin.IN)  # Left (off the line) sensor
        self.sensor_middle_left = Pin(12, Pin.IN)  # Middle left (on the line) sensor
        self.sensor_middle_right = Pin(10, Pin.IN)  # Middle right (on the line) sensor
        self.sensor_right = Pin(13, Pin.IN)  # Right (off the line) sensor
        
        # CONTROL
        self.Kp = 10  # constant
        self.Ki = 0.1  # constant
        self.turning_kp = 0
        self.turning_ki = 0
        self.speed = 80  # constant
        self.integral_tau = 0.05  # constant
        self.integral_timer = 0
        
        # NAVIGATION
        self.coming_from = "L"
        self.going_to = "C"
        self.position = 0
        self.current_path = PATHS[self.coming_from+self.going_to]
        self.next_turn = ""
        
        # TURNING
        self.turning = False
        self.turn_time = 0
        
        
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
        self.L_motor.speed(self.speed)
        self.R_motor.speed(self.speed)

    def proportional(self): # proportion control for line following
        if self.s_lineML == 1 and self.s_lineMR == 0:  # too right
            self.turning_kp = self.Kp
        elif self.s_lineML == 0 and self.s_lineMR == 1:  # too left
            self.turning_kp = -self.Kp
        else:
            self.turning_kp = 0

    def integral(self): # integral control for line following 
        if time.time() - self.integral_timer > 2:
            self.integral_timer = time.time()
            # set 0?
        elif time.time() - self.integral_timer < self.integral_tau:
            pass
        else:
            if self.turning_kp > 0:
                self.turning_ki += self.Ki
            elif self.turning_kp < 0:
                self.turning_ki -= self.Ki
            self.integral_timer = time.time()

    def follow_line(self):

        if self.s_lineML == 1 or self.s_lineMR == 1:
            self.proportional()
            self.integral()
            self.bank(self.turning_kp + self.turning_ki)
        else:
            # Off the line
            pass
        
    def turn(self, direction):
        #direction = "left" # this has been included for testing. In the future this will be retrieved from a navigation module
        
        # allow time for centre of turning of bot to reach junction (need to experimentally tune this time)
        #if time.time() - self.turn_time < 1.3:
            #self.follow_line()
        
        # turn the bot
        #else:
        min_turning_time = 0.3
        if direction == "left":
            self.L_motor.speed(-75)
            self.R_motor.speed(75) 
        elif direction == "right":
            self.L_motor.speed(75)
            self.R_motor.speed(-75)
        else: #going straight
            self.update_sensors()
            self.follow_line()
            min_turning_time+=.5

        # stop turning when middle sensor reads the line again (needs adjusting to make sure the correct sensor is used)
        if (time.time() - self.turn_time > min_turning_time):
            if (direction == "right" and self.s_lineML == 1) or (direction == "left" and self.s_lineMR == 1) or direction == "straight":
                print("Stopped turning")
                self.turning = False
                time.sleep(.15)
            
         
    def drive(self):
        
        self.update_sensors()

        if not self.turning: # if not turning, follow the line straight
            self.follow_line()
            
            if (self.s_lineL == 1 or self.s_lineR == 1): # if the far left/right sensors detect a junction, trigger turning sequence
                if (self.position < len(self.current_path)):
                    self.turn_time = time.time()
                    self.turning = True
                    self.next_turn = self.current_path[self.position]
                    self.position += 1
                    print("started turning")
                else:
                    self.L_motor.speed(0)
                    self.R_motor.speed(0)
                    self.cargo()
                
        if self.turning:
            self.turn(self.next_turn)
    
    def cargo(self):
        # Should handle re-assigning directions and current path
        pass

    def run(self):
        while self.running:
            self.drive()
            self.cargo()





