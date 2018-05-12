#! /usr/lib/python

#import curses
#from curses import wrapper
from tts import *
from lib import *
from rotarySeqShort import *

import smbus
import time

#import argparse
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
CHATTER_BUS = smbus.SMBus(0)
CHATTER_ADDRESS_BUS = 0x12
CHATTER_USERNAME = "ENZO"

CHATTER_LANG = "fr-FR" # fr-FR or us-EN
CHATTER_LANG_SHORT = "FR" # FR or EN
CHATTER_INTERACTION_MODE = "ROTARY" # ROTARY or KEYBOARD
CHATTER_TERMINAL = False

CHATTER_COLOR_BLACK = 0
CHATTER_COLOR_RED = 1
CHATTER_COLOR_GREEN = 2
CHATTER_COLOR_YELLOW = 3
CHATTER_COLOR_CYAN = 6
CHATTER_COLOR_DEFAULT = 9


########
# MENU
########

def menu(lang, dico):
	FSC_MENU = ["Fisher Price Chatter\n\n",
            "---| MENU |-------------------------------\n",
            dico["MENU1"].format(CHATTER_USERNAME),
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
 
def gmailMessageHeader(dico):
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
        logOutput(dico["NOLABEL"],CHATTER_COLOR_YELLOW)
    else:
        if PRINT_CATEGORY: logOutput(dico["GMAIL_LABEL"],CHATTER_COLOR_YELLOW)
        for label in labels:
            if PRINT_CATEGORY: logOutput(label['name'],CHATTER_COLOR_YELLOW)
            if label['name']=='UNREAD':
                listMessages = ListMessagesWithLabels(service, 'me', label['name'])
                nbMessages = len(listMessages)
                nbMess = 0
                if(nbMessages!=0) and not(CHATTER_TERMINAL):
                    CHATTER_BUS.write_byte(CHATTER_ADDRESS_BUS, 1)
                    time.sleep(1)

                logOutput(dico["MSG"].format(nbMessages),CHATTER_COLOR_YELLOW)
                #say('ENZO! Tu as: '+str(nbMessages)+' messages non lus.')
                say(dico["MSG"].format(nbMessages),CHATTER_LANG)
                for message in listMessages:
                    #print(GetMessage(service, 'me', message['id'], False))
                    nbMess+=1
                    ggMessage = GetMessage(service, 'me', message['id'], False)
                    #print(ggMessage)
                    for header in ggMessage['payload']['headers']:
                        #print(header)
                        if header['name']=='Subject':
                            logOutput(str(nbMess)+'] '+header['value'],CHATTER_COLOR_YELLOW)
                            say(header['value'],CHATTER_LANG)
                    while True:
                        try:
                            event = str(raw_input(' ['+time.strftime("%c")+'] :  '+dico["INPUT"]+" : "))
                        except ValueError:
                            logOutput(dico["BREAK"],CHATTER_COLOR_RED)

                        if event == ord("q") or  event == "q" :
                            logOutput(dico["BREAK"],CHATTER_COLOR_RED)
                            return

                        elif event ==  ord("t") or event == "t" :
                            logOutput(dico["GMAIL_MENUS"],CHATTER_COLOR_RED)
                            TrashMessage(service, 'me', message['id'])
                            break

                        elif event ==  ord("n") or event == "n" :
                            logOutput(dico["GMAIL_MENUN"],CHATTER_COLOR_RED)
                            break


    
def  writeBus(stdscr,):
    stdscr.clear()
    stdscr.addstr("\n\n")
    printTerminal(dico["HELLOWORLD"],stdscr,False)
    stdscr.addstr("\n\n")
    printMenu(stdscr, FSC_MENU[1:])

def color(code,background=False):
    if background:
        print('\033[4{}m'.format(code)),
    else:
        print('\033[3{}m'.format(code)),

def logOutput(log,colorOutput):
    color(colorOutput)
    print('['+time.strftime("%c")+'] :'),
    color(CHATTER_COLOR_DEFAULT)
    print(log)

def inputMenu(dico):
    error = True
    while error:
        try:
            # color(CHATTER_COLOR_GREEN)
            inputValue = str(raw_input(' ['+time.strftime("%c")+'] :  '+dico["INPUT"]+" : "))
            # color(CHATTER_COLOR_DEFAULT)
            error = False
        except ValueError:
            logOutput(dico["BREAK"],CHATTER_COLOR_RED)
    return inputValue

#def main(stdscr, terminal=True):
def main():

    dicoHistory = i8n.i8n()
    dico = dicoHistory.dico(CHATTER_LANG_SHORT)
    menu = dicoHistory.menu(CHATTER_LANG_SHORT)

    logOutput(dico["CHATTER_PHONE"],CHATTER_COLOR_CYAN)
    CHATTER_BUS.write_byte(CHATTER_ADDRESS_BUS, 8)

    #say('Bonjour '+CHATTER_USERNAME+', comment vas-tu?')
    logOutput(dico["HELLO"].format(CHATTER_USERNAME),CHATTER_COLOR_CYAN)
    say(dico["HELLO"].format(CHATTER_USERNAME),CHATTER_LANG)
    logOutput(dico["MENU"].format(CHATTER_USERNAME),CHATTER_COLOR_CYAN)
    say(dico["MENU"].format(CHATTER_USERNAME),CHATTER_LANG)




    while True:
        if CHATTER_TERMINAL:
            # logOutput(dico["INPUT"],CHATTER_COLOR_CYAN)
            for menuKey, menuValue in menu:
                logOutput(menuValue,CHATTER_COLOR_DEFAULT)
            event = inputMenu(dico)
            print ""
        else:
            #rotarySeqShort.rotaryAction.rotary()
            rotaryAction = rotarySeqShort()
            #event = rotaryAction.rotary()
            event = rotaryAction.rotaryMenuPush()

        if event == ord("q") or  event == "q" or  event == "3" :
            logOutput(dico["BREAK"],CHATTER_COLOR_RED)
            #break
            time.sleep(1)

        elif event ==  ord("1") or event == "1" :
            logOutput(dico["MENU1"].format(CHATTER_USERNAME),CHATTER_COLOR_RED)
            gmailMessageHeader(dico)

        elif event == ord("2") or event == "2" :
            historyPlay = history.history()
            logOutput(dico["STORYTITLE"].format(historyPlay.text()[0]),CHATTER_COLOR_CYAN)
            logOutput(dico["STORYTITLE"].format(historyPlay.text()[1]),CHATTER_COLOR_CYAN)

            historyPlay.read(CHATTER_LANG)

        elif event ==  ord("3") or event == "3" :
            logOutput(dico["HELLOWORLD"],CHATTER_COLOR_CYAN)
            say(dico["HELLOWORLD"],CHATTER_LANG)
            time.sleep(1)
            logOutput(dico["ALWAYSHERE"],CHATTER_COLOR_CYAN)
            say(dico["ALWAYSHERE"],CHATTER_LANG)

        elif event == ord("4") or event == "4" :
            CHATTER_BUS.write_byte(CHATTER_ADDRESS_BUS, 4)
            logOutput(dico["TERMINATOR"],CHATTER_COLOR_CYAN)
            say(dico["TERMINATOR"],CHATTER_LANG)

        elif event == ord("5") or event == "5" :
            logOutput(dico["BYPASS"],CHATTER_COLOR_RED)

        elif event == ord("6") or event == "6" :
            logOutput(dico["BUS_WRITE"].format(CHATTER_ADDRESS_BUS, 6),CHATTER_COLOR_CYAN)
            CHATTER_BUS.write_byte(CHATTER_ADDRESS_BUS, 6)
            time.sleep(1)

        elif event == ord("V") or event == "V" :
            logOutput(dico["BUS_WRITE"].format(CHATTER_ADDRESS_BUS, 6),CHATTER_COLOR_CYAN)
            CHATTER_BUS.write_byte(CHATTER_ADDRESS_BUS, 6)
            time.sleep(1)

    #stdscr.refresh()
    #stdscr.getkey()

if __name__ == '__main__':
    main()
    #gmail(False)
    #wrapper(main)