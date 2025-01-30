from machine import ADC

class Distance:
    
    def __init__(self):

        self.sensor_pin = ADC(26)  # SIG pin connected to GPIO 26 (adjust as necessary)

    def get_distance(self):
        # Read the ADC value 
        self.raw_value = self.sensor_pin.read_u16()  
        self.voltage = self.raw_value * 3.3 / 65535  # Convert to voltage
        # range 500cm
        self.distance = (self.voltage * 500) / 3.3  # distance in cm
        return self.distance
