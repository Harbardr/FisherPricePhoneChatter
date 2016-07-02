#! /usr/lib/python

import curses
from curses import wrapper
from gmail import *
from tts import *
from lib import *
from rotaryPhone import *

import smbus
import time
# Remplacer 0 par 1 si nouveau Raspberry
bus = smbus.SMBus(0)
address = 0x12

#from servo import *

import locale
locale.setlocale(locale.LC_ALL,"")

FSC_MENU = ["Fisher Price Chatter\n\n",
            "---| MENU |-------------------------------\n",
            "1] Read Enzo emails\n",
            "2] Print hello world!\n",
            "3] Blabla car\n",
            "4] Wink eyes\n",
            "5] i2c test\n",
            "6] i2c Blink test\n",
            "\nq] Quit\n",
            "------------------------------------------\n"]
            
def printTerminal(text,object,header=False):
    lenText = len(text)+4
    if header: object.addstr('#'*lenText+'\n')
    if header:
        borderLeft = '# '
        borderRight = ' #'
    else:
        borderLeft = ''
        borderRight = ''
    #object.addstr(borderLeft+text.encode("ascii","ignore")+borderRight+'\n')
    object.addstr(borderLeft+text.encode('utf_8')+borderRight+'\n')
    if header: object.addstr('#'*lenText+'\n')
    object.refresh()

def printMenu(stdscr, fscMenu):
    for iMenu in fscMenu:
        stdscr.addstr(iMenu)

def functionTest(stdscr, toto):
    printTerminal(toto,stdscr,False)
    for i in range(2, 11):
        v = i-1
        stdscr.addstr('10 divided by {} is {}\n'.format(v, 10/v))
 
def gmailMessageHeader(screen):
    """Shows basic usage of the Gmail API. and more #!
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        printTerminal('No labels found.',screen,True)
    else:
        if PRINT_CATEGORY: printTerminal('Labels:',screen,False)
        for label in labels:
            if PRINT_CATEGORY: printTerminal(label['name'],screen,False)
            if label['name']=='UNREAD':
                listMessages = ListMessagesWithLabels(service, 'me', label['name'])
                nbMessages = len(listMessages)
                nbMess = 0
                if(nbMessages!=0):
                    bus.write_byte(address, 1)
                    time.sleep(1)

                printTerminal('ENZO! Tu as ['+str(nbMessages)+'] messages non lus.',screen,True)
                say('ENZO! Tu as: '+str(nbMessages)+' messages non lus.')
                for message in listMessages:
                    #print(GetMessage(service, 'me', message['id'], False))
                    nbMess+=1
                    ggMessage = GetMessage(service, 'me', message['id'], False)
                    #print(ggMessage)
                    for header in ggMessage['payload']['headers']:
                        #print(header)
                        if header['name']=='Subject':
                            printTerminal(str(nbMess)+'] '+header['value'],screen,False)
                            say(header['value'])
    
        
def main(stdscr):
    # Clear screen
    say('Bonjour ENZO, comment vas-tu?')
    stdscr.clear()
    printMenu(stdscr, FSC_MENU)

    while True:
        #event = stdscr.getch()
        
        rotaryAction = rotaryPhone()
        event = rotaryAction.rotary()
        if(event!=None):print(event)
        
        if event == ord("q"): break
        elif event ==  ord("1"):
            stdscr.clear()
            gmailMessageHeader(stdscr)
            stdscr.addstr("\n\n")
            printMenu(stdscr, FSC_MENU[1:])
        elif event ==  ord("2"):
            stdscr.clear()
            printTerminal("HELLO WORLD",stdscr,False)
            stdscr.addstr("\n\n")
            printMenu(stdscr, FSC_MENU[1:])
        elif event == ord("3"):
            stdscr.clear()
            asciiCar(stdscr)
            stdscr.addstr("\n\n")
            printMenu(stdscr, FSC_MENU[1:])
            # #stdscr.clear()
            # for ind in range(1,100):
                # #stdscr.addstr(ind, 0, 'toto is dead {}'.format(ind))
                # print('\ntoto is dead {}'.format(ind))
                # #stdscr.clear()
            # stdscr.addstr("\n\nPress b to go back")
            # while True:
                # event2 = stdscr.getch()
                # if event2 == ord("b"):
                    # stdscr.clear()
                    # break
        # elif event == curses.KEY_DOWN:
            # stdscr.clear()
            # stdscr.addstr("The User Pressed DOWN")
        elif event == ord("4"):
            stdscr.clear()
            eyes()
            stdscr.addstr("\n\n")
            printMenu(stdscr, FSC_MENU[1:])
        elif event == ord("5"):
	    stdscr.clear()
            printTerminal("Envoi de la valeur 3",stdscr,False)
            stdscr.addstr("\n\n")
            bus.write_byte(address, 3)
            # Pause de 1 seconde pour laisser le temps au traitement de se faire
            time.sleep(1)
            reponse = bus.read_byte(address)
            while reponse == 0:
                time.sleep(100)
            	reponse = bus.read_byte(address)
            stdscr.clear()
            printTerminal("La reponse de l'arduino : " + str(reponse),stdscr,False)
            stdscr.addstr("\n\n")

            printMenu(stdscr, FSC_MENU[1:])
        elif event == ord("6"):
	    stdscr.clear()
            printTerminal("Envoi de la valeur 6",stdscr,False)
            stdscr.addstr("\n\n")
            bus.write_byte(address, 6)
            # Pause de 1 seconde pour laisser le temps au traitement de se faire
            time.sleep(1)
            printMenu(stdscr, FSC_MENU[1:])
        elif event == "6":
	    stdscr.clear()
            printTerminal("Envoi de la valeur 6",stdscr,False)
            stdscr.addstr("\n\n")
            bus.write_byte(address, 6)
            # Pause de 1 seconde pour laisser le temps au traitement de se faire
            time.sleep(1)
            printMenu(stdscr, FSC_MENU[1:])
  
    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    #main()
    #gmail(False)
    wrapper(main)
