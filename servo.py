# !/usr/bin/python
import time
import RPi.GPIO as GPIO
from RPIO import PWM

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
PWM.setup()
PWM.init_channel(0)

def eyes(wink=3):
	for i in (1,wink):
		PWM.add_channel_pulse(0, 17, 0, 10)
		time.sleep(1)
		PWM.add_channel_pulse(0, 17, 0, 100)
		time.sleep(1)
		PWM.clear_channel_gpio(0, 17)
		GPIO.cleanup()

if __name__ == '__main__':
	while True : 
		#for i in range(100,201):
		PWM.add_channel_pulse(0, 17, 0, 10)
		time.sleep(1)
		PWM.add_channel_pulse(0, 17, 0, 100)
		time.sleep(1)
		PWM.add_channel_pulse(0, 17, 200, 100)
		time.sleep(1)
		PWM.clear_channel_gpio(0, 17)
		GPIO.cleanup()
