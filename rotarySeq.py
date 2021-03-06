#! /usr/lib/python

# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

import gaugette.rotary_encoder
import gaugette.switch
import time

class rotarySeq(object):

    def __init__(self):

        self.A_PIN  = 2
        self.B_PIN  = 3
        self.SW_PIN = 0

    def numbers(self, number, longNumber=False):
        if number == "9":
            print ("------------")
            print ("-  888888  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  888888  -")
            print ("-      88  -")
            if(longNumber): print ("-     88   -")
            print ("-  888888  -")
            print ("------------")
        if number == "8":
            print ("------------")
            print ("-  888888  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  888888  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  888888  -")
            print ("------------")
        if number == "7":
            print ("------------")
            print ("-  888888  -")
            if(longNumber): print ("-      88  -")
            print ("-     88   -")
            print ("-    88    -")
            if(longNumber): print ("-    88    -")
            print ("-    88    -")
            print ("-    88    -")
            print ("------------")
        if number == "6":
            print ("------------")
            print ("-  888888  -")
            print ("-  88      -")
            if(longNumber): print ("-  88      -")
            print ("-  888888  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  888888  -")
            print ("------------")
        if number == "5":
            print ("------------")
            print ("-  888888  -")
            print ("-  88      -")
            if(longNumber): print ("-  88      -")
            print ("-  888888  -")
            print ("-      88  -")
            if(longNumber): print ("-      88  -")
            print ("-  888888  -")
            print ("------------")
        if number == "4":
            print ("------------")
            print ("-  88  88  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  888888  -")
            print ("-      88  -")
            if(longNumber): print ("-      88  -")
            print ("-      88  -")
            print ("------------")
        if number == "3":
            print ("------------")
            print ("-  888888  -")
            print ("-      88  -")
            if(longNumber): print ("-      88  -")
            print ("-  888888  -")
            print ("-      88  -")
            if(longNumber): print ("-      88  -")
            print ("-  888888  -")
            print ("------------")
        if number == "2":
            print ("------------")
            print ("-  888888  -")
            print ("-      88  -")
            if(longNumber): print ("-      88  -")
            print ("-  888888  -")
            print ("-  88      -")
            if(longNumber): print ("-  88      -")
            print ("-  888888  -")
            print ("------------")
        if number == "1":
            print ("------------")
            print ("-      88 -")
            print ("-    8888  -")
            if(longNumber): print ("-  88  88  -")
            print ("-      88  -")
            print ("-      88  -")
            if(longNumber): print ("-      88  -")
            print ("-      88  -")
            print ("------------")
        if number == "0":
            print ("------------")
            print ("-  888888  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  88  88  -")
            print ("-  88  88  -")
            if(longNumber): print ("-  88  88  -")
            print ("-  888888  -")
            print ("------------")


    def rotary(self):

        sw_state = 0
        last_state = 0
        select_state = 0
        return_state = 0
        phoneNumber = ""
        sequenceNumber = ""
        longNumber = False

        encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(self.A_PIN, self.B_PIN)
        encoder.start()
        switch = gaugette.switch.Switch(self.SW_PIN)

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
                    #print ("rotate %d = (9)" % select_state)
                    #numbers("9",longNumber)
                    sequenceNumber = "9"
                    return "%s" % sequenceNumber
                elif select_state <= 81 and select_state > 71:
                    #print ("rotate %d = (8)" % select_state)
                    #numbers("8",longNumber)
                    sequenceNumber = "8"
                    return "%s" % sequenceNumber
                elif select_state <= 71 and select_state > 61:
                    #print ("rotate %d = (7)" % select_state)
                    #numbers("7",longNumber)
                    sequenceNumber = "7"
                    return "%s" % sequenceNumber
                elif select_state <= 61 and select_state > 51:
                    #print ("rotate %d = (6)" % select_state)
                    #numbers("6",longNumber)
                    sequenceNumber = "6"
                    return "%s" % sequenceNumber
                elif select_state <= 51 and select_state > 41:
                    #print ("rotate %d = (5)" % select_state)
                    #numbers("5",longNumber)
                    sequenceNumber = "5"
                    return "%s" % sequenceNumber
                elif select_state <= 41 and select_state > 31:
                    #print ("rotate %d = (4)" % select_state)
                    #numbers("4",longNumber)
                    sequenceNumber = "4"
                    return "%s" % sequenceNumber
                elif select_state <= 31 and select_state > 21:
                    #print ("rotate %d = (3)" % select_state)
                    #numbers("3",longNumber)
                    sequenceNumber = "3"
                    return "%s" % sequenceNumber
                elif select_state <= 21 and select_state > 11:
                    #print ("rotate %d = (2)" % select_state)
                    #numbers("2",longNumber)
                    sequenceNumber = "2"
                    return "%s" % sequenceNumber
                elif select_state <= 11 and select_state > 0:
                    #print ("rotate %d = (1)" % select_state)
                    #numbers("1",longNumber)
                    sequenceNumber = "1"
                    return "%s" % sequenceNumber
                if return_state > 0 and return_state < 5:
                    #print ("== REINITIALISATION ==")
                    sequenceNumber = "0"
                    return "%s" % sequenceNumber
                phoneNumber = phoneNumber + sequenceNumber
                #print(phoneNumber)
                sequenceNumber=""
                select_state=0
                return_state=0
                
            sw_state = switch.get_state()
            #print ("switch %d - %d" % sw_state, last_state)
            #print (sw_state)
            #print(last_state)
            if (sw_state != last_state and last_state != None):
                #print ("switch %d" % sw_state)
                last_state = sw_state
                
                return "V"
                #if phoneNumber != "":
                    #print("%s" % phoneNumber)
                    #return "%s" % phoneNumber
                    
        encoder.stop()
