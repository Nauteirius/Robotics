import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
pi_pwm = GPIO.PWM(12, 1000)
pi_pwm.start(0)
for i in range(100):
    print("LED on")
    pi_pwm.ChangeFrequency(1)
    time.sleep(1)
    print("LED off")
    pi_pwm.ChangeFrequency(100)
    time.sleep(1)