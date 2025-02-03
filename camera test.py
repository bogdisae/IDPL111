from CAMERA import Camera
import time

camera = Camera()

while True:
    camera.detect_qr_code()  
    if camera.detected_qr:
        print("QR Code Detected: ", camera.message_string)  
    else:
        print("No QR code detected.")
    time.sleep(1)  
