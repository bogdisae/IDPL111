from BOT import Bot
import time
from machine import Pin

bot = Bot()
button = Pin(22, Pin.IN, Pin.PULL_DOWN)


while True:
    if button.value() == 1:
        bot.forward()
        bot.run()
        break












