import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.output(2,0)
time.sleep(3)
GPIO.output(2,1)
time.sleep(3)
GPIO.output(2,0)
time.sleep(3)
GPIO.output(2,1)
time.sleep(3)
GPIO.output(2,0)