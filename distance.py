import machine
import time

# Set up the pin connected to the sensor's signal (SIG) pin (adjust based on your connection)
sensor_pin = machine.ADC(26)  # Assume SIG is connected to GPIO 26

# Function to read and calculate the distance from the sensor
def get_distance():
    # Read the ADC value (ranging from 0 to 65535)
    raw_value = sensor_pin.read_u16()  
    # Convert the ADC value to voltage (assuming a 3.3V power supply)
    voltage = raw_value * 3.3 / 65535  # Convert ADC value to voltage
    # Assume linear relation between voltage and distance:
    # The sensor output range is from 0V to 3.3V, corresponding to a distance of 2cm to 500cm
    # We map the voltage to the distance (max range = 500 cm)
    distance = (voltage * 500) / 3.3  # Calculate the distance (in cm)
    return distance

# Main loop to repeatedly measure and print the distance
while True:
    distance = get_distance()
    print("Distance: {:.2f} cm".format(distance))  # Print the calculated distance
    time.sleep(1)  # Wait for 1 second before measuring again
