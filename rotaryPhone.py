# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground.
# The sw_pin should be shorted to ground by the switch.

import gaugette.rotary_encoder
import gaugette.switch
import time

class rotaryPhone(object):

    def __init__(self):

        self.A_PIN  = 2
        self.B_PIN  = 3
        self.SW_PIN = 0

        self.sw_state = 0
        self.last_state = 0
        self.select_state = 0
        self.return_state = 0
        self.phoneNumber = ""
        self.sequenceNumber = ""
        self.longNumber = False


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
        
        #A_PIN  = 7
        #B_PIN  = 9
        #SW_PIN = 8
        
        #A_PIN  = 2
        #B_PIN  = 3
        #SW_PIN = 0
        
        encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(self.A_PIN, self.B_PIN)
        encoder.start()
        switch = gaugette.switch.Switch(self.SW_PIN)
        
        #sw_state = 0
        #last_state = 0
        #select_state = 0
        #return_state = 0
        #phoneNumber = ""
        #sequenceNumber = ""
        #longNumber = False
        while True:
            delta = encoder.get_delta()
            #if delta!=0:
                #print ("rotate %d" % delta)
            if delta<0:
                self.select_state+=delta
                #print ("rotate %d" % select_state)
            if delta>0:
                self.return_state+=delta
            if self.return_state > 10:
                self.select_state = abs(self.select_state)
                if self.select_state <= 91 and self.select_state > 81:
                    print ("rotate %d = (9)" % self.select_state)
                    self.numbers("9",self.longNumber)
                    self.sequenceNumber = "9"
                elif self.select_state <= 81 and self.select_state > 71:
                    print ("rotate %d = (8)" % self.select_state)
                    self.numbers("8",self.longNumber)
                    self.sequenceNumber = "8"
                elif self.select_state <= 71 and self.select_state > 61:
                    print ("rotate %d = (7)" % self.select_state)
                    self.numbers("7",self.longNumber)
                    self.sequenceNumber = "7"
                elif self.select_state <= 61 and self.select_state > 51:
                    print ("rotate %d = (6)" % self.select_state)
                    self.numbers("6",self.longNumber)
                    self.sequenceNumber = "6"
                elif self.select_state <= 51 and self.select_state > 41:
                    print ("rotate %d = (5)" % self.select_state)
                    self.numbers("5",self.longNumber)
                    self.sequenceNumber = "5"
                elif self.select_state <= 41 and self.select_state > 31:
                    print ("rotate %d = (4)" % self.select_state)
                    self.numbers("4",self.longNumber)
                    self.sequenceNumber = "4"
                elif self.select_state <= 31 and self.select_state > 21:
                    print ("rotate %d = (3)" % self.select_state)
                    self.numbers("3",self.longNumber)
                    self.sequenceNumber = "3"
                elif self.select_state <= 21 and self.select_state > 11:
                    print ("rotate %d = (2)" % self.select_state)
                    self.numbers("2",self.longNumber)
                    self.sequenceNumber = "2"
                elif self.select_state <= 11 and self.select_state > 0:
                    print ("rotate %d = (1)" % self.select_state)
                    self.numbers("1",self.longNumber)
                    self.sequenceNumber = "1"
                if self.return_state > 0 and self.return_state < 5:
                    print ("== REINITIALISATION ==")
                self.phoneNumber = self.phoneNumber + self.sequenceNumber
                print(self.phoneNumber)
                self.sequenceNumber=""
                self.select_state=0
                self.return_state=0
                
            self.sw_state = switch.get_state()
            #print ("switch %d - %d" % sw_state, last_state)
            #print (sw_state)
            #print(last_state)
            if (self.sw_state != self.last_state and self.last_state != None):
                #print ("switch %d" % sw_state)
                self.last_state = self.sw_state
                if self.phoneNumber != "":
                    return self.phoneNumber
                    
        encoder.stop()
