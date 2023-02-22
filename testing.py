import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
for i in range(100):
    print("LED on")
    GPIO.output(12,GPIO.HIGH)
    time.sleep(1)
    print("LED off")
    GPIO.output(12,GPIO.LOW)
    time.sleep(1)