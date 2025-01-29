import struct
import time
import machine
import distance  # Import the distance module
import servo     # Import the servo module

# QR Code Reader Setup
TINY_CODE_READER_I2C_ADDRESS = 0x0C
TINY_CODE_READER_DELAY = 0.05
TINY_CODE_READER_LENGTH_OFFSET = 0
TINY_CODE_READER_LENGTH_FORMAT = "H"
TINY_CODE_READER_MESSAGE_OFFSET = TINY_CODE_READER_LENGTH_OFFSET + struct.calcsize(TINY_CODE_READER_LENGTH_FORMAT)
TINY_CODE_READER_MESSAGE_SIZE = 254
TINY_CODE_READER_MESSAGE_FORMAT = "B" * TINY_CODE_READER_MESSAGE_SIZE
TINY_CODE_READER_I2C_FORMAT = TINY_CODE_READER_LENGTH_FORMAT + TINY_CODE_READER_MESSAGE_FORMAT
TINY_CODE_READER_I2C_BYTE_COUNT = struct.calcsize(TINY_CODE_READER_I2C_FORMAT)

# Initialize I2C for QR Code Reader
i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18), freq=400000)

def detect_qr_code():
    while True:
        time.sleep(TINY_CODE_READER_DELAY)
        read_data = i2c.readfrom(TINY_CODE_READER_I2C_ADDRESS, TINY_CODE_READER_I2C_BYTE_COUNT)
        message_length, = struct.unpack_from(TINY_CODE_READER_LENGTH_FORMAT, read_data, TINY_CODE_READER_LENGTH_OFFSET)
        message_bytes = struct.unpack_from(TINY_CODE_READER_MESSAGE_FORMAT, read_data, TINY_CODE_READER_MESSAGE_OFFSET)

        if message_length == 0:
            print('No QR code detected')
            continue
        try:
            message_string = bytearray(message_bytes[0:message_length]).decode("utf-8")
            print('QR Code Detected:', message_string)

            # When a QR code is detected, trigger the distance measurement and servo activation
            distance_value = distance.get_distance()
            print("Measured Distance:", distance_value)
            if distance_value <= 5:
                servo.activate_servo()

        except Exception as e:
            print("Error decoding QR code:", e)
            pass
