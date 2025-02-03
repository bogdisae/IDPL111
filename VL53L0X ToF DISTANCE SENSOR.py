from machine import Pin, I2C
import time
import vl53l0x

i2c = I2C(0, scl=Pin(10), sda=Pin(11), freq=400000)  # I2C pins and frequency
# Initialize the VL53L0X sensor
sensor = vl53l0x.VL53L0X(i2c)

sensor.start()

while True:
    distance = sensor.read()
    if distance > 0:  # If valid distance reading
        print("Distance: {} mm".format(distance))
    else:
        print("Error reading distance.")
    time.sleep(1)  # Wait for 1 second before the next reading
