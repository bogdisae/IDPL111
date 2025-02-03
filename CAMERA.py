import struct
import time
import machine

   
class Camera:

    def __init__(self):
        self.detected_qr = False

        # QR Code Reader Setup
        self.TINY_CODE_READER_I2C_ADDRESS = 0x0C
        self.TINY_CODE_READER_DELAY = 0.05
        self.TINY_CODE_READER_LENGTH_OFFSET = 0
        self.TINY_CODE_READER_LENGTH_FORMAT = "H"
        self.TINY_CODE_READER_MESSAGE_OFFSET = self.TINY_CODE_READER_LENGTH_OFFSET + struct.calcsize(self.TINY_CODE_READER_LENGTH_FORMAT)
        self.TINY_CODE_READER_MESSAGE_SIZE = 254
        self.TINY_CODE_READER_MESSAGE_FORMAT = "B" * self.TINY_CODE_READER_MESSAGE_SIZE
        self.TINY_CODE_READER_I2C_FORMAT = self.TINY_CODE_READER_LENGTH_FORMAT + self.TINY_CODE_READER_MESSAGE_FORMAT
        self.TINY_CODE_READER_I2C_BYTE_COUNT = struct.calcsize(self.TINY_CODE_READER_I2C_FORMAT)

        # Initialize I2C for QR Code Reader
        self.i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18), freq=400000)

    def detect_qr_code(self):
        self.detected_qr = False

        time.sleep(self.TINY_CODE_READER_DELAY)
        self.read_data = self.i2c.readfrom(self.TINY_CODE_READER_I2C_ADDRESS, self.TINY_CODE_READER_I2C_BYTE_COUNT)
        self.message_length, = struct.unpack_from(self.TINY_CODE_READER_LENGTH_FORMAT, self.read_data, self.TINY_CODE_READER_LENGTH_OFFSET)
        self.message_bytes = struct.unpack_from(self.TINY_CODE_READER_MESSAGE_FORMAT, self.read_data, self.TINY_CODE_READER_MESSAGE_OFFSET)
        
        if self.message_length != 0:
            try:
                self.message_string = bytearray(self.message_bytes[0:self.message_length]).decode("utf-8")
                self.detected_qr = True
                time.sleep(3)

            except Exception as e:
                #print("Error decoding QR code:", e)
                pass





