#from Tkinter import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

while True:
   GPIO.output(pin, GPIO.HIGH)  
   time.sleep(0.0015)  
   GPIO.output(pin, GPIO.LOW)  
   time.sleep(0.0185)
