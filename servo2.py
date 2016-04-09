#from Tkinter import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(5)

#while True:
#   GPIO.output(18, GPIO.HIGH)  
#   time.sleep(0.0015)  
#   GPIO.output(18, GPIO.LOW)  
#   time.sleep(0.0185)
