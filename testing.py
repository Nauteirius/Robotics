import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
pi_pwm = GPIO.PWM(12, 1000)
pi_pwm.start(1)
for i in range(1000):
    pi_pwm.ChangeFrequency(i)
    time.sleep(0.1)
pi_pwm.stop()
GPIO.cleanup()