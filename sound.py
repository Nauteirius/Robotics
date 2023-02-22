from time import sleep
import os
import time
from RPi import GPIO


GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM
GPIO.setup(16, GPIO.OUT)# set GPIO 16 as an output. You can use any GPIO port
p = GPIO.PWM(16, 200)    # create an object p for PWM on port 16 at 50 Hertz
p.start(70)             # start the PWM on 70 percent duty cycle
for x in range(200, 2200):
      p.ChangeFrequency(x)  # change the frequency to x Hz (
      time.sleep(0.0001)
p.stop()                # stop the PWM output
GPIO.cleanup()          # when your program exits, tidy up after yourself