from machine import Pin
from PATHS import PATHS
from MOTOR import Motor
from CAMERA import Camera
from ToF_SENSOR import ToF
from SERVO import Servo
#from LIGHT import Light
import time
   
class Bot:
    def __init__(self):
        
        # MOTORS
        self.R_motor = Motor(4, 5)  # Right Motor
        self.L_motor = Motor(7, 6)  # Left Motor

        # CARGO
        self.camera = Camera()
        self.tof = ToF()
        self.servo = Servo()
        self.boxes_at_L = 4
        self.boxes_at_R = 4

        # LINE SENSORS
        self.sensor_left = Pin(11, Pin.IN)  # Left (off the line) sensor
        self.sensor_middle_left = Pin(12, Pin.IN)  # Middle left (on the line) sensor
        self.sensor_middle_right = Pin(10, Pin.IN)  # Middle right (on the line) sensor
        self.sensor_right = Pin(9, Pin.IN)  # Right (off the line) sensor
        
        # CONTROL
        self.Kp = 8  # constant
        self.Ki = 0.1  # constant
        self.turning_kp = 0
        self.turning_ki = 0
        self.speed = 90  # constant
        self.integral_tau = 0.05  # constant
        self.integral_timer = 0
        
        # NAVIGATION
        self.coming_from = "H"
        self.going_to = "L"
        self.position = 0
        self.current_path = PATHS[self.coming_from+self.going_to]
        self.turn_direction = ""
                
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
        
        print(f"turning {direction}")

        timer = time.time()

        while True:
            self.update_sensors()
            min_turning_time = 0.35 # used to ensure sensors aren't triggered immediately after starting the turn.
        

            if direction == "left":
                self.L_motor.speed(-40)
                self.R_motor.speed(100) 

            elif direction == "right":
                self.L_motor.speed(100)
                self.R_motor.speed(-40)

            else: #going straight
                self.follow_line()

            # stop turning when middle sensors read the line again
            if direction != 'straight':
                if (time.time() - timer > min_turning_time) and (self.s_lineML == 1 and self.s_lineMR == 1):
                    break
            
            elif self.s_lineL == 0 and self.s_lineR == 0:
                break
            

    def spin_around(self, direction): # used for turning around on the spot

        timer = time.time()

        while True:
            self.update_sensors()
            min_turning_time = 0.6

            if direction == "left":
                self.L_motor.speed(-100)
                self.R_motor.speed(100) 

            elif direction == "right":
                self.L_motor.speed(100)
                self.R_motor.speed(-100)

            # stop turning when middle sensors read the line again 
            if (time.time() - timer > min_turning_time):
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
                    pass


    def cargo_dropoff(self):

        # reassign going to variable
        if self.boxes_at_L != 0: # if there are still boxes at R, then return to R
            self.going_to = 'L'
        
        elif self.boxes_at_R != 0: # if there are no boxes at R, but still boxes at L, go to L
            self.going_to = 'R'

        else: # we have dropped off all the boxes, return to home
            self.going_to = 'H'

        self.current_path = PATHS[self.coming_from+self.going_to]

        while True:
            self.update_sensors()
            self.follow_line()

            if self.s_lineL == 1 or self.s_lineR == 1: # outer sensors detected depot dropoff 
                
                # dropoff the box
                self.stop()
                time.sleep(1)
                self.servo.turn_to_angle(0)
                time.sleep(1)
                break

        # reverse back and turn when reached the line
        self.reverse(85)
        timer = time.time()
        
        while True:
            self.update_sensors()
            if (time.time() - timer > 1) and (self.s_lineL == 1 or self.s_lineR == 1):
                self.turn_direction = self.current_path[0]
                if self.turn_direction == 'right': # since reversing, we want the robot to turn in the opposite direction
                    self.turn('left')
                else:
                    self.turn('right')

                self.position += 1
                break
            
    
    def cargo_pickup(self):

        # first determine the number of boxes removed from depot (used for sensor delays later on)
        if self.going_to == 'L':
            boxes_removed = 4 - self.boxes_at_L
        else:
            boxes_removed = 4 - self.boxes_at_R
        
        self.speed = 50
        timer = time.time() 

        while True: # Drive forward slowly, constantly trying to scan the qr
            self.update_sensors()
            self.follow_line()
            self.camera.detect_qr_code()

            if self.camera.detected_qr: 
                print(f"QR Code Detected: {self.camera.message_string}")
                self.going_to = self.camera.message_string[0]
                break
            
            if time.time() - timer > 5:
                print("QR Code detection failed, defaulting to A.")
                self.going_to = 'A' # return location A if the camera cant read anything after 5 seconds
                break
        

        while True: # now we know where we are going, drive forward and pick up the box
            self.update_sensors()
            self.follow_line()
            
            
            if self.tof.get_distance() < 10: # the box is in the cargo hold
                print("detected cargo")
                self.stop()
                time.sleep(1)
                self.servo.turn_to_angle(20)
                time.sleep(1)
                break
        
        self.speed = 85

        # reassign path 
        self.current_path = PATHS[self.coming_from+self.going_to]    

        # Once the box has been picked up, reverse back for an amount of time dependent on the number of boxes left.
        # This is to avoid turning on the box pickup lines
        reverse_time = 0.5 + 1*boxes_removed # 0.5 seconds + 1 second for every box that has been removed from that depot.
        self.reverse(85)
        time.sleep(reverse_time)

        # A direction has been specified to avoid hitting the side walls.
        if self.coming_from == 'L':
            self.spin_around('left')
        else:
            self.spin_around('right')


    def run(self):
        while self.running:
            self.drive()













