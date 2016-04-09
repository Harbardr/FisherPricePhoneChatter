# !/usr/bin/python
import time
import RPi.GPIO as GPIO
from RPIO import PWM

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
PWM.setup()
PWM.init_channel(0)
while True : 
	for i in range(100,201):
		PWM.add_channel_pulse(0, 17, 0, i)
		time.sleep(0.05)
		PWM.add_channel_pulse(0, 17, 100, i)
		time.sleep(0.05)
