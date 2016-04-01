import curses
from curses import wrapper
from gmail import *
from tts import *

import locale
locale.setlocale(locale.LC_ALL,"")

FSC_MENU = ["Fisher Price Chatter\n\n",
            "---| MENU |-------------------------------\n",
            "1] Read Enzo emails\n",
            "2] Print hello world!\n",
            "3] Blabla car\n",
            "\nq] Quit\n",
            "------------------------------------------\n"]

def asciiCar(stdscr):
    stdscr.addstr("         _____________________\n")
    stdscr.addstr("        //~~~~~~~~~~~~~~~~~~~\\\\\n")
    stdscr.addstr("       //                     \\\\\n")
    stdscr.addstr("      //_______________________\\\\\n")
    stdscr.addstr("    /  /                       \\  \\\n")
    stdscr.addstr("   /  /                         \\  \\\n")
    stdscr.addstr("  /__/___________________________\\__\\\n")
    stdscr.addstr(" |/| ____ ||||||||||||||||||| ____ |\\|\n")
    stdscr.addstr(" |/|______|||||||DODGE|||||||______|\\|\n")
    stdscr.addstr(" |/ ||  |||||||||||||||||||||||  || \\|\n")
    stdscr.addstr("/-------------------------------------\\\n")
    stdscr.addstr(" ------------------------------------- \n")
    stdscr.addstr(" |\_________________________________/|\n")
    stdscr.addstr(" |     |                       |     |\n")
    stdscr.addstr(" |_____|                       |_____|\n")
            
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

        
 
def gmail(screen):
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
                printTerminal('ENZO! Tu as ['+str(nbMessages)+'] messages non lus.',screen,True)
                say('ENZO! Tu as: '+str(nbMessages)+' messages non lus.')
                for message in listMessages:
                    #print(GetMessage(service, 'me', message['id'], False))
                    nbMess+=1
                    ggMessage = GetMessage(service, 'me', message['id'], False)
                    #print(ggMessage)
                    #msg_str = base64.urlsafe_b64decode(ggMessage['raw'].encode('ASCII'))
                    #print(msg_str)
                    for header in ggMessage['payload']['headers']:
                        #print(header)
                        if header['name']=='Subject':
                            #unicode(text,'utf-8')
                            #screen.addstr(0,1,"")
                            #screen.addstr(str(nbMess)+'] '+header['value'])
                            printTerminal(str(nbMess)+'] '+header['value'],screen,False)
                            # time.sleep(2)
                            #screen.refresh()
                            say(header['value'])

                    #for part in ggMessage['payload']['parts']:
                    #    msg = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII'))
                    #    print(removehtml(msg))
                        #print(part['body']['data'])
                        # #say(part['body']['data'])
                    # if len(sys.argv) > 1:
                        # if sys.argv[1]=='-t':
                            # TTS(ggMessage,'french', 50 ,2 )
                    #for toto in label:
                    #  print(toto)   
    
        
def prg(stdscr):
    # Clear screen

    stdscr.clear()
    printMenu(stdscr, FSC_MENU)

    while True:
        event = stdscr.getch()
        if event == ord("q"): break
        elif event ==  ord("1"):
            stdscr.clear()
            gmail(stdscr)
            #functionTest(stdscr, "You have [4] messages")
            stdscr.addstr("\n\n")
            printMenu(stdscr, FSC_MENU[1:])
            #stdscr.keypad(1)
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
    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    #main()
    #gmail(False)
    wrapper(prg)
