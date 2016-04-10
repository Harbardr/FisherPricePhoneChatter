# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

import gaugette.rotary_encoder
import gaugette.switch

A_PIN  = 7
B_PIN  = 9
SW_PIN = 8

encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None

select_state = 0
return_state = 0

def numbers(number, short=False):
    if number == 9:
        print ("------------")
        print ("-  888888  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  888888  -")
        print ("-      88  -")
        if(!short): print ("-     88   -")
        print ("-  888888  -")
        print ("------------")
    if number == 8:
        print ("------------")
        print ("-  888888  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  888888  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  888888  -")
        print ("------------")
    if number == 7:
        print ("------------")
        print ("-  888888  -")
        if(!short): print ("-      88  -")
        print ("-     88   -")
        print ("-    88    -")
        if(!short): print ("-    88    -")
        print ("-    88    -")
        print ("-    88    -")
        print ("------------")
    if number == 6:
        print ("------------")
        print ("-  888888  -")
        print ("-  88      -")
        if(!short): print ("-  88      -")
        print ("-  888888  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  888888  -")
        print ("------------")
    if number == 5:
        print ("------------")
        print ("-  888888  -")
        print ("-  88      -")
        if(!short): print ("-  88      -")
        print ("-  888888  -")
        print ("-      88  -")
        if(!short): print ("-      88  -")
        print ("-  888888  -")
        print ("------------")
    if number == 4:
        print ("------------")
        print ("-  88  88  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  888888  -")
        print ("-      88  -")
        if(!short): print ("-      88  -")
        print ("-      88  -")
        print ("------------")
    if number == 3:
        print ("------------")
        print ("-  888888  -")
        print ("-      88  -")
        if(!short): print ("-      88  -")
        print ("-  888888  -")
        print ("-      88  -")
        if(!short): print ("-      88  -")
        print ("-  888888  -")
        print ("------------")
    if number == 2:
        print ("------------")
        print ("-  888888  -")
        print ("-      88  -")
        if(!short): print ("-      88  -")
        print ("-  888888  -")
        print ("-  88      -")
        if(!short): print ("-  88      -")
        print ("-  888888  -")
        print ("------------")
    if number == 1:
        print ("------------")
        print ("-      88 -")
        print ("-    8888  -")
        if(!short): print ("-  88  88  -")
        print ("-      88  -")
        print ("-      88  -")
        if(!short): print ("-      88  -")
        print ("-      88  -")
        print ("------------")
    if number == 0:
        print ("------------")
        print ("-  888888  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  88  88  -")
        print ("-  88  88  -")
        if(!short): print ("-  88  88  -")
        print ("-  888888  -")
        print ("------------")


short = True
while True:
    delta = encoder.get_delta()
    #if delta!=0:
        #print ("rotate %d" % delta)
    if delta<0:
        select_state+=delta
        #print ("rotate %d" % select_state)
    if delta>0:
        return_state+=delta
    if return_state > 10:
        select_state = abs(select_state)
        if select_state <= 91 and select_state > 81:
            print ("rotate %d = (9)" % select_state)
            numbers(9,short)
        elif select_state <= 81 and select_state > 71:
            print ("rotate %d = (8)" % select_state)
            numbers(8,short)
        elif select_state <= 71 and select_state > 61:
            print ("rotate %d = (7)" % select_state)
            numbers(7,short)
        elif select_state <= 61 and select_state > 51:
            print ("rotate %d = (6)" % select_state)
            numbers(6,short)
        elif select_state <= 51 and select_state > 41:
            print ("rotate %d = (5)" % select_state)
            numbers(5,short)
        elif select_state <= 41 and select_state > 31:
            print ("rotate %d = (4)" % select_state)
            numbers(4,short)
        elif select_state <= 31 and select_state > 21:
            print ("rotate %d = (3)" % select_state)
            numbers(3,short)
        elif select_state <= 21 and select_state > 11:
            print ("rotate %d = (2)" % select_state)
            numbers(2,short)
        elif select_state <= 11 and select_state > 0:
            print ("rotate %d = (1)" % select_state)
            numbers(1,short)
        if return_state > 0 and return_state < 5:
            print ("== REINITIALISATION ==")
        select_state=0
        return_state=0
        
    sw_state = switch.get_state()
    if sw_state != last_state:
        print ("switch %d" % sw_state)
        last_state = sw_state
