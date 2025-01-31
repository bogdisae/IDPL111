from CAMERA import Camera
from DISTANCE import Distance
from SERVO import Servo
import time

class Cargo:

    def __init__(self):
        self.cargo_detected = False

        self.dist_sensor = Distance() # distance sensor
        self.camera = Camera() # camera/QR scanner
        self.servo = Servo() # servo motor


    def detect_cargo(self):
        if self.dist_sensor.get_distance() < 2: # distnace in cm
            self.cargo_detected = True
            