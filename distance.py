from machine import ADC

class Distance:
    
    def __init__(self):

        self.sensor_pin = ADC(26)  # SIG pin connected to GPIO 26 (adjust as necessary)

    def get_distance(self):
        # Read the ADC value 
        self.raw_value = self.sensor_pin.read_u16()  
        self.distance = (self.raw_value * 500) / 65535.0  # distance in cm
        sleep (0.2)
        return self.distance
