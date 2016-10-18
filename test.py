#! /usr/lib/python

import curses
from curses import wrapper
from tts import *
from lib import *
from rotarySeq import *

import smbus
import time

import argparse
import locale
locale.setlocale(locale.LC_ALL,"")

#from servo import *
import history
import i8n

from gmail import *
########
# ARG
########


#TO check
#stdscr = curses.initscr()
#End TO Check


########
# VAR
########

# Remplacer 0 par 1 si nouveau Raspberry
bus = smbus.SMBus(0)
address = 0x12
userName = "ENZO"

CHATTER_USERNAME = "ENZO"

CHATTER_LANG = "fr-FR" # fr-FR or us-EN
CHATTER_LANG_SHORT = "FR" # FR or EN
CHATTER_INTERACTION_MODE = "ROTARY" # ROTARY or KEYBOARD
CHATTER_TERMINAL = True



########
# MENU
########

def menu(lang, dico):
	FSC_MENU = ["Fisher Price Chatter\n\n",
            "---| MENU |-------------------------------\n",
            dico["MENU1"].format(userName),
            dico["MENU2"],
            dico["MENU3"],
            dico["MENU4"],
            dico["MENU5"],
            dico["MENU6"],
            dico["MENUV"],
            dico["MENUQ"],
            "------------------------------------------\n"]
	return FSC_MENU
            
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
        #printTerminal('No labels found.',screen,True)
        printTerminal(dico["NOLABEL"],screen,True)
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

                #printTerminal('ENZO! Tu as ['+str(nbMessages)+'] messages non lus.',screen,True)
                printTerminal(dico["MSG"].format(nbMessages),screen,True)
                #say('ENZO! Tu as: '+str(nbMessages)+' messages non lus.')
                say(dico["MSG"].format(nbMessages),lang)
                for message in listMessages:
                    #print(GetMessage(service, 'me', message['id'], False))
                    nbMess+=1
                    ggMessage = GetMessage(service, 'me', message['id'], False)
                    #print(ggMessage)
                    for header in ggMessage['payload']['headers']:
                        #print(header)
                        if header['name']=='Subject':
                            printTerminal(str(nbMess)+'] '+header['value'],screen,False)
                            say(header['value'],lang)
    
def  writeBus():
    


#def main(stdscr, terminal=True):
def main(stdscr):
    # Clear screen

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-r", "--rotary", action="store_true", help="Use the encoder")
    # parser.add_argument("-k", "--keyboard", action="store_true", help="Use the keyboard")
    # parser.add_argument("-lg", "--lang", action="store", help="French language")
    # args = parser.parse_args()
    
    dicoHistory = i8n.i8n()
    dico = dicoHistory.dico(CHATTER_LANG_SHORT)

    # if args.lang.lower() == "en":
    #    dico = dicoHistory.dico("EN")
    #    lang = "en-US"
    #else:
    #    dico = dicoHistory.dico("FR")
    #    lang = "fr-FR"

    if CHATTER_INTERACTION_MODE == "ROTARY":
        CHATTER_TERMINAL = False
    
    #say('Bonjour '+userName+', comment vas-tu?')
    say(dico["HELLO"].format(userName),CHATTER_LANG)

    if CHATTER_TERMINAL:
        stdscr.clear()
        FSC_MENU = menu(CHATTER_LANG_SHORT, dico)
        printMenu(stdscr, FSC_MENU)
    else:
        rotaryAction = rotarySeq()

    while True:
        if CHATTER_TERMINAL:
            stdscr.clear()
            event = stdscr.getch()
        else:
            rotaryAction.rotary()
        #if(event!=None):
        #    print(event)

        if event == ord("q"): break
        elif event ==  ord("1") or event == "1" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                #gmailMessageHeader(stdscr)
                stdscr.addstr("\n\n")
                printMenu(stdscr, FSC_MENU[1:])
        elif event ==  ord("2") or event == "2" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                stdscr.addstr("\n\n")
                printTerminal(dico["HELLOWORLD"],stdscr,False)
                stdscr.addstr("\n\n")
                printMenu(stdscr, FSC_MENU[1:])
            else:
                say(dico["HELLOWORLD"],CHATTER_LANG)
                time.sleep(1)
                say(dico["ALWAYSHERE"],CHATTER_LANG)
        elif event == ord("3") or event == "3" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                asciiCar(stdscr)
                stdscr.addstr("\n\n")
                printMenu(stdscr, FSC_MENU[1:])
            else:
                say(dico["BACKTOTHEFUTUR"],CHATTER_LANG)

        elif event == ord("4") or event == "4" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                eyes()
                stdscr.addstr("\n\n")
                printMenu(stdscr, FSC_MENU[1:])
        elif event == ord("5") or event == "5" :
            history = history()
            if CHATTER_TERMINAL:
                stdscr.clear()
                title, text = history.text()
                #printTerminal("Read history : {}".format(title),stdscr,False)
                printTerminal(dico["STORYTITLE"].format(title),stdscr,False)
                stdscr.addstr("\n\n")
                printTerminal(dico["STORYTEXT"].format(text),stdscr,False)
                stdscr.addstr("\n\n")
                history.read(CHATTER_LANG)
                stdscr.clear()
                printMenu(stdscr, FSC_MENU[1:])
            else:
                history.read(CHATTER_LANG)

        elif event == ord("6") or event == "6" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                printTerminal("Envoi de la valeur 6",stdscr,False)
                stdscr.addstr("\n\n")
                bus.write_byte(address, 6)
                time.sleep(1)
                printMenu(stdscr, FSC_MENU[1:])
            else:
                bus.write_byte(address, 6)
                time.sleep(1)
        elif event == ord("6") or event == "6" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                printTerminal("Envoi de la valeur 6",stdscr,False)
                stdscr.addstr("\n\n")
                bus.write_byte(address, 6)
                time.sleep(1)
                printMenu(stdscr, FSC_MENU[1:])
            else:
                bus.write_byte(address, 6)
                time.sleep(1)
        elif event == ord("V") or event == "V" :
            if CHATTER_TERMINAL:
                stdscr.clear()
                printTerminal(dico["VALIDATION"],stdscr,False)
                stdscr.addstr("\n\n")
                bus.write_byte(address, 6)
                time.sleep(1)
                printMenu(stdscr, FSC_MENU[1:])
            else:
                bus.write_byte(address, 6)
                time.sleep(1)

    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    #main()
    #gmail(False)
    wrapper(main)
