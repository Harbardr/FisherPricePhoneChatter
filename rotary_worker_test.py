# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

import gaugette.rotary_encoder
import gaugette.switch

#A_PIN  = 7
#B_PIN  = 9
#SW_PIN = 8

#CHange for the PINS

A_PIN  = 2
B_PIN  = 3
SW_PIN = 0
    
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None


menu = ["Menu 1","Menu 2","Menu 3"]

index = 0
print (menu[index])

while True:
    delta = encoder.get_delta()
    if delta!=0:
        #print ("rotate %d" % delta)
        index = index + int(delta)
        if index > 2:
            index = 0
        if index < 0:
            index = 2
        print (menu[index])


    sw_state = switch.get_state()
    if sw_state != last_state:
        print ("switch %d" % sw_state)
        last_state = sw_state
