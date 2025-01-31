from MOTOR import Motor
from BOT import Bot
from machine import Pin, PWM
from utime import sleep
import camera
import distance


bot = Bot()

bot.run()

camera.detect_qr_code()







