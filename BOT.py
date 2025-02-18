from machine import Pin
from PATHS import PATHS, PATHS_TESTING
from MOTOR import Motor
from CAMERA import Camera
from ToF_SENSOR import ToF
from SERVO import Servo
from LIGHT import Light
import time

TESTING = False
first_turn = "L"
if TESTING:
    PATHS = PATHS_TESTING

class Bot:
    def __init__(self):
        
        # MOTORS
        self.R_motor = Motor(4, 5)  # Right Motor
        self.L_motor = Motor(7, 6, 0.95)  # Left Motor

        # CARGO
        self.camera = Camera()
        self.tof = ToF()
        self.servo = Servo()
        self.boxes_at_L = 1
        self.boxes_at_R = 4

        # LINE SENSORS
        self.sensor_left = Pin(11, Pin.IN)  # Left (off the line) sensor
        self.sensor_middle_left = Pin(12, Pin.IN)  # Middle left (on the line) sensor
        self.sensor_middle_right = Pin(10, Pin.IN)  # Middle right (on the line) sensor
        self.sensor_right = Pin(9, Pin.IN)  # Right (off the line) sensor
        
        # CONTROL
        self.Kp = 20  # constant
        self.turning_kp = 0
        self.speed = 100  # constant
      
        # NAVIGATION
        self.coming_from = "H"
        self.going_to = first_turn
        self.position = 0
        self.current_path = PATHS[self.coming_from+self.going_to]
        self.turn_direction = ""
                
        self.running = True
        self.light = Light()
        self.reduce = 0

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

    def reverse(self, rev_speed):
        self.L_motor.speed(-1*rev_speed)
        self.R_motor.speed(-1*rev_speed)

    def stop(self):
        self.L_motor.speed(0)
        self.R_motor.speed(0)

    def proportional(self): # proportion control for line following
        if self.s_lineML == 1 and self.s_lineMR == 0:  # too right
            self.turning_kp = self.Kp
        elif self.s_lineML == 0 and self.s_lineMR == 1:  # too left
            self.turning_kp = -self.Kp
        elif self.s_lineML == 1 and self.s_lineMR == 1:  # too left
            self.turning_kp = 0


    def follow_line(self):
        self.proportional()
        self.bank(self.turning_kp)
        
    def turn(self, direction):

        timer = time.ticks_ms()
        min_turning_time = 900

        while True:
            self.update_sensors()

            if direction == "left":
                self.L_motor.speed(-50)
                self.R_motor.speed(100) 

            elif direction == "right":
                self.L_motor.speed(100)
                self.R_motor.speed(-50)

            else: #going straight
                self.follow_line()

            # stop turning when middle sensors read the line again
            if direction != 'straight':
                if (time.ticks_ms() - timer > min_turning_time) and (self.s_lineML == 1 and self.s_lineMR == 1):
                    break
            
            elif self.s_lineL == 0 and self.s_lineR == 0:
                break
            

    def spin_around(self, direction): # used for turning around on the spot

        timer = time.ticks_ms()
        min_turning_time = 900

        while True:
            self.update_sensors()

            if direction == "left":
                self.L_motor.speed(-100)
                self.R_motor.speed(100) 

            elif direction == "right":
                self.L_motor.speed(100)
                self.R_motor.speed(-100)

            # stop turning when middle sensors read the line again 
            if (time.ticks_ms() - timer > min_turning_time):
                if (self.s_lineML == 1 and self.s_lineMR == 1):
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

                    # keep track of how many boxes are at each pickup
                    if self.coming_from == 'L':
                        self.boxes_at_L -= 1
                    elif self.coming_from == 'R':
                        self.boxes_at_R -= 1
                
                elif self.going_to in "ABCD": # the bot is at a dropoff point
                    self.cargo_dropoff()

                else: # the bot is returning home
                    time.sleep(0.5)
                    self.light.off()
                    self.stop()
                    time.sleep(100)

    def get_dropoff_time(self, destination = "A", reduce = 0):
        if destination == "A":
            return 1500 - reduce
        elif destination == "B":
            return 1081 - reduce
        elif destination == "C":
            return 1500 - reduce
        elif destination == "D":
            return 1300 - reduce
        
    def cargo_dropoff(self):
        
        reduce_at_end = False

        # reassign going to variable
        if first_turn == "L":    
            if self.boxes_at_L != 0: # if there are still boxes at L, then return to L
                self.going_to = 'L'
            elif self.boxes_at_R != 0: # if there are no boxes at L, but still boxes at R, go to R
                self.going_to = 'R'
                reduce_at_end = True
        else:
            if self.boxes_at_R != 0: # if there are still boxes at R, then return to R
                self.going_to = 'R'
            elif self.boxes_at_L != 0: # if there are no boxes at R, but still boxes at L, go to L
                self.going_to = 'L'
                reduce_at_end = True
                
        if self.boxes_at_L == 0 and self.boxes_at_R == 0:
            self.going_to = 'H'

        self.current_path = PATHS[self.coming_from+self.going_to]
        
        timer = time.ticks_ms()

        while True:
            self.update_sensors()
            self.follow_line()

            #if self.s_lineL == 1 or self.s_lineR == 1: # outer sensors detected depot dropoff
            if time.ticks_ms() - timer > self.get_dropoff_time(self.coming_from, self.reduce):
                
                # dropoff the box
                self.stop()
                #time.sleep(1)
                self.servo.turn_to_angle(87.5)
                #time.sleep(1)
                break
        
        # reverse back and turn when reached the line
        self.reverse(100)
        timer = time.ticks_ms()
        
        while True:
            self.update_sensors()
            if (time.ticks_ms() - timer > 750) and (self.s_lineL == 1 or self.s_lineR == 1):
                self.turn_direction = self.current_path[0]
                if self.turn_direction == 'right': # since reversing, we want the robot to turn in the opposite direction
                    self.turn('left')
                else:
                    self.turn('right')

                self.position += 1
                break
            
        self.servo.turn_to_angle(0)
        
        if reduce_at_end:
            self.reduce = 500
            
    
    def cargo_pickup(self):
        self.servo.turn_to_angle(87.5)

        # first determine the number of boxes removed from depot (used for sensor delays later on)
        if self.going_to == 'L':
            boxes_removed = 4 - self.boxes_at_L
        else:
            boxes_removed = 4 - self.boxes_at_R
        
        self.speed = 60
        timer = time.ticks_ms() 

        while True: # Drive forward slowly, constantly trying to scan the qr
            self.update_sensors()
            self.follow_line()
            self.camera.detect_qr_code()

            if self.camera.detected_qr: 
                #print(f"QR Code Detected: {self.camera.message_string}")
                self.going_to = self.camera.message_string[0]
                break
            
            if time.ticks_ms() - timer > 2000:
                #print("QR Code detection failed, defaulting to C.")
                self.going_to = 'C' # return location C if the camera cant read anything after 1.5 seconds
                break
        

        self.speed = 100
        
        timer = time.ticks_ms()
        
        while True: # now we know where we are going, drive forward and pick up the box
            self.update_sensors()
            self.follow_line()
            
            
            if self.tof.get_distance() < 10 and time.ticks_ms() - timer > 300: # the box is in the cargo hold
                self.stop()
                #time.sleep(1)
                self.servo.turn_to_angle(40)
                #time.sleep(1)
                break

        # reassign path 
        self.current_path = PATHS[self.coming_from+self.going_to]    

        # Once the box has been picked up, reverse back for an amount of time dependent on the number of boxes left.
        # This is to avoid turning on the box pickup lines
        reverse_time = 0.3 + 0.2*boxes_removed # 0.3 seconds + 0.4 second for every box that has been removed from that depot.
        self.reverse(100)
        time.sleep(reverse_time)

        # A direction has been specified to avoid hitting the side walls.
        if self.coming_from == 'L':
            self.spin_around('left')
        else:
            self.spin_around('right')


    def run(self):
        self.servo.turn_to_angle(0)
        self.light.on()
        while self.running:
            self.drive()



