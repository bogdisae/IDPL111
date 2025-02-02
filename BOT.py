from machine import Pin
from MOTOR import Motor
from CARGO import Cargo
from CAMERA import Camera
from DISTANCE import Distance
from SERVO import Servo
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

        # CARGO
        self.camera = Camera()
        self.dist_sensor = Distance()
        self.servo = Servo()
        self.cargo_time = 0

        # LINE SENSORS
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
        self.turn_direction = ""
        
        # TURNING
        self.turning = False
        self.turn_time = 0
        
        # CARGO handling 
        self.cargo = Cargo()
        
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

        self.turn_time = time.time()

        while True:
            self.update_sensors()

            min_turning_time = 0.3
            if direction == "left":
                self.L_motor.speed(-75)
                self.R_motor.speed(75) 
            elif direction == "right":
                self.L_motor.speed(75)
                self.R_motor.speed(-75)
            else: #going straight
                self.follow_line()
                min_turning_time+=.5

            # stop turning when middle sensor reads the line again (needs adjusting to make sure the correct sensor is used)
            if (time.time() - self.turn_time > min_turning_time):
                if (direction == "right" and self.s_lineML == 1) or (direction == "left" and self.s_lineMR == 1) or direction == "straight":
                    time.sleep(.15)
                    break
            
         
    def drive(self):
        
        self.update_sensors()
        self.follow_line()
            
        # if the far left/right sensors detect a junction, trigger turning sequence    
        if (self.s_lineL == 1 or self.s_lineR == 1) and (self.position < len(self.current_path)): 
            self.turn_direction = self.current_path[self.position]
            self.position += 1
            self.turn(self.turn_direction)

        if self.position == len(self.current_path): # handle cargo pickup / dropoff, and path reassignment
            self.coming_from = self.going_to
            self.position = 0

            if self.going_to in "LR": # the bot is at a pickup point
                self.cargo_pickup()
            
            else: # the bot is at a dropoff point
                self.cargo_dropoff()
        
            self.current_path = PATHS[self.coming_from+self.going_to]


    def cargo_dropoff(self):
        pass            
    
    def cargo_pickup(self):

        self.update_sensors()
        self.follow_line()

        if self.dist_sensor.get_distance() < 2: # distnace in cm
            self.cargo_time = time.time()
            while True:
                self.camera.detect_qr_code()

                if self.camera.detected_qr:
                    self.going_to = self.camera.message_string[0]
                    break
                
                if time.time() - self.timer > 5:
                    self.going_to = 'A' # return location A if the camera cant read anything after 5 seconds
                    break
            
            # function to drive forward and pick up the box

            self.turn('right') # turn around and carry on
        

    def run(self):
        while self.running:
            self.drive()
            self.cargo()





