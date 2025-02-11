# import time
from machine import Pin, I2C
from VL53L0X import VL53L0X

class ToF:
    
    def __init__(self):

        self.i2c = I2C(id=0, sda=Pin(16), scl=Pin(17))

        # print("creating vl53lox object")
        # Create a VL53L0X object
        self.tof = VL53L0X(self.i2c)

        # Pre: 12 to 18 (initialized to 14 by default)
        # Final: 8 to 14 (initialized to 10 by default)

        # the measuting_timing_budget is a value in ms, the longer the budget, the more accurate the reading. 
        self.budget = self.tof.measurement_timing_budget_us
        self.tof.set_measurement_timing_budget(40000)

        # Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the 
        # given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange) 
        # to the given value (in PCLKs). Longer periods increase the potential range of the sensor. 
        # Valid values are (even numbers only):

        # tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
        self.tof.set_Vcsel_pulse_period(self.tof.vcsel_period_type[0], 12)

        # tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
        self.tof.set_Vcsel_pulse_period(self.tof.vcsel_period_type[1], 8)


    def get_distance(self):
        return self.tof.ping()-50

