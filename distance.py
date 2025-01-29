import machine

sensor_pin = machine.ADC(26)  # SIG pin connected to GPIO 26 (adjust as necessary)

def get_distance():
    # Read the ADC value 
    raw_value = sensor_pin.read_u16()  
    voltage = raw_value * 3.3 / 65535  # Convert to voltage
    # range 500cm
    distance = (voltage * 500) / 3.3  # distance in cm
    return distance
