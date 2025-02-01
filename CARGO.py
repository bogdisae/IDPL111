from CAMERA import Camera
from DISTANCE import Distance
from SERVO import Servo
import time

class Cargo:

    def __init__(self):
        self.cargo_detected = False
        self.timer = 0

        self.dist_sensor = Distance() # distance sensor
        self.camera = Camera() # camera/QR scanner
        self.servo = Servo() # servo motor


    def detect_cargo(self): 
        if self.dist_sensor.get_distance() < 2: # distnace in cm
            self.cargo_detected = True
            self.timer = time.time()

    def get_destination_from_qr(self): # return the destination from qr
        while True:        
            self.camera.detect_qr_code()
            
            if self.camera.detected_qr:
                return self.camera.message_string[0]
            
            if time.time() - self.timer > 5:
                return 'A' # return location A if the camera cant read anything after 5 seconds
            
    
        



