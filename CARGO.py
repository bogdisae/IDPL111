from CAMERA import Camera
from DISTANCE import Distance
from SERVO import 
import time

class Cargo:

    def __init__(self):
        self.cargo_detected = False

        self.dist_sensor = Distance() # distance sensor
        self.camera = Camera() # camera/QR scanner




    def detect_cargo(self):
        if 