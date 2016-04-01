from __future__ import print_function
import httplib2
import os

import sys
import pyttsx
import time
import base64

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

import subprocess
import re

import curses
from curses import wrapper

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '/home/pi/FisherPrice/client_secret.json'
APPLICATION_NAME = 'FisherPriceChatter'

PRINT_CATEGORY = False
GMAIL_UNREAD = 0

def printTerminal(text,header=False):
    lenText = len(text)+4
    if header: print('#'*lenText)
    print('# '+text+' #')
    if header: print('#'*lenText)

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    #home_dir = os.path.expanduser('~')
    home_dir = os.path.expanduser('/home/pi/')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials




def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
           page_token = response['nextPageToken']
           response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
           messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.
    Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id, snippetMessage=True):
    """Get a Message with given ID.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.
    Returns:
        A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        #print('Message snippet: %s' % message['snippet'])
        #print('Message snippet: %s' % message['payload']['headers'])
        #print(unicode('Message snippet: %s' % message['snippet'],'utf-8'))

        if snippetMessage:
            return message['snippet']
        else:
            return message
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def TTS(text, voice='french', rate=0, volume=0):
    # use sys.argv if needed
    engine = pyttsx.init('espeak')
    #engine.startLoop(False)
    volumeTTS = engine.getProperty('volume')
    engine.setProperty('volume', volumeTTS+volume)
    engine.setProperty('voice', voice)
    rateTTS = engine.getProperty('rate')
    engine.setProperty('rate', rateTTS-rate)
    #str = unicode(text,'utf-8')
    str = text
    #if len(sys.argv) > 1:
    #    str = sys.argv[1]
    engine.say(str)
    engine.runAndWait()
    while engine.isBusy():
        time.sleep(1)    
    while engine.isBusy():
        print(engine.isBusy())
    engine.stop()

def say(words, lang='fr-FR'):
    tempfile = "temp.wav"
    devnull = open("/dev/null","w")
    subprocess.call(["pico2wave", '--lang='+lang, "-w", tempfile, words],stderr=devnull)
    subprocess.call(["aplay", tempfile],stderr=devnull)
    os.remove(tempfile)

def removehtml(html):
    p = re.compile(r'^(<!DOCTYPE html>).+(</html>)$', re.MULTILINE|re.DOTALL)
    return p.sub('',html)



# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):

    # work out what text to display as the last menu option
    if parent is None:
        lastoption = "Exit"
    else:
        lastoption = "Return to %s menu" % parent['title']

    optioncount = len(menu['options']) # how many options in this menu

    pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
    oldpos=None # used to prevent the screen being redrawn every time
    x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

    # Loop until return key is pressed
    while x !=ord('\n'):
        if pos != oldpos:
            oldpos = pos
            screen.border(0)
            screen.addstr(2,2, menu['title'], curses.A_STANDOUT) # Title for this menu
            screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu

            # Display all the menu items, showing the 'pos' item highlighted
            for index in range(optioncount):
                textstyle = n
                if pos==index:
                    textstyle = h
                screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
            # Now display Exit/Return at bottom of menu
            textstyle = n
            if pos==optioncount:
                textstyle = h
            screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
            screen.refresh()
            # finished updating screen

        x = screen.getch() # Gets user input

        # What is user input?
        if x >= ord('1') and x <= ord(str(optioncount+1)):
            pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
        elif x == 258: # down arrow
            if pos < optioncount:
                pos += 1
            else: pos = 0
        elif x == 259: # up arrow
            if pos > 0:
                pos += -1
            else: pos = optioncount
    # return index of the selected item
    return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
    optioncount = len(menu['options'])
    exitmenu = False
    while not exitmenu: #Loop until the user exits the menu
        getin = runmenu(menu, parent)
        if getin == optioncount:
            exitmenu = True
        elif menu['options'][getin]['type'] == COMMAND:
            curses.def_prog_mode()    # save curent curses environment
            os.system('reset')
            if menu['options'][getin]['title'] == 'Pianobar':
                os.system('amixer cset numid=3 1') # Sets audio output on the pi to 3.5mm headphone jack
            screen.clear() #clears previous screen
            os.system(menu['options'][getin]['command']) # run the command
            screen.clear() #clears previous screen on key press and updates display based on pos
            curses.reset_prog_mode()   # reset to 'current' curses environment
            curses.curs_set(1)         # reset doesn't do this right
            curses.curs_set(0)
            os.system('amixer cset numid=3 2') # Sets audio output on the pi back to HDMI

        elif menu['options'][getin]['type'] == COMMAND_PYTHON:
            screen.clear() #clears previous screen on key press and updates display based on pos
            process_network_command(menu['options'][getin]['command'], '22') # l
            screen.clear() #clears previous screen on key press and updates display based on pos      
        elif menu['options'][getin]['type'] == MENU:
            screen.clear() #clears previous screen on key press and updates display based on pos
            processmenu(menu['options'][getin], menu) # display the submenu
            screen.clear() #clears previous screen on key press and updates display based on pos
        elif menu['options'][getin]['type'] == EXITMENU:
            exitmenu = True






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
        print('No labels found.')
    else:
        if PRINT_CATEGORY: print('Labels:')
        for label in labels:
            if PRINT_CATEGORY: print(label['name'])
            if label['name']=='UNREAD':
                listMessages = ListMessagesWithLabels(service, 'me', label['name'])
                nbMessages = len(listMessages)
                nbMess = 0

                printTerminal('ENZO! Tu as ['+str(nbMessages)+'] messages non lus.',True)
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
                            if screen:
                                screen.addstr(str(nbMess)+'] '+header['value'])
                                say(header['value'])
                                screen.refresh()
                            else:
                                print(str(nbMess)+'] '+header['value'])
                                say(header['value'])
                            #TTS(header['value'],'french', 50 ,2 )
                            #status=subprocess.call(["espeak","-s 100 -v fr ",header['value']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    #for part in ggMessage['payload']['parts']:
                    #    msg = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII'))
                    #    print(removehtml(msg))
                        #print(part['body']['data'])
                        #say(part['body']['data'])
                    if len(sys.argv) > 1:
                        if sys.argv[1]=='-t':
                            TTS(ggMessage,'french', 50 ,2 )
                    #for toto in label:
                    #  print(toto)

def main():
    screen = curses.initscr()
    curses.endwin()
    curses.flash()
    curses.noecho()
    #curses.nonl()
    curses.curs_set(0)
    screen.keypad(1)

    screen.addstr("This is a Sample Curses Script\n\n")

    screen.addstr("1] Read Enzo emails\n")
    screen.addstr("2] Print hello world!\n")

    while True:
        event = screen.getch()
        if event == ord("q"): break
        elif event ==  ord("1"):
            screen.clear()
            gmail(screen)
            screen.keypad(1)
        elif event ==  ord("2"):
            screen.clear()
            screen.addstr("The User Pressed 1")
            screen.keypad(1)
        elif event == curses.KEY_UP:
            screen.clear()
            screen.addstr("The User Pressed UP")
            i = 0
            screen.clear()
            while i < 100:
                i+=1
                screen.addstr('toto is dead: '+str(i))
                screen.keypad(1)
            screen.addstr("\n\nPress b to go back")  
            
            while True:
                event2 = screen.getch()
                if event2 == ord("b"): 
                    screen.clear()
                    break
                    
        elif event == curses.KEY_DOWN:
            screen.clear()
            screen.addstr("The User Pressed DOWN")
       
    curses.endwin()

def prg(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i-10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.addstr("This is a Sample Curses Script\n\n")
    stdscr.addstr("1] Read Enzo emails\n")
    stdscr.addstr("2] Print hello world!\n")
 
    while True:
        event = stdscr.getch()
        if event == ord("q"): break
        elif event ==  ord("1"):
            stdscr.clear()
            #gmail(stdscr)
            stdscr.keypad(1)
        elif event ==  ord("2"):
            stdscr.clear()
            stdscr.addstr("The User Pressed 1")
            stdscr.keypad(1)
        elif event == curses.KEY_UP:
            stdscr.clear()
            stdscr.addstr("The User Pressed UP")
            i = 0
            stdscr.clear()
            while i < 100:
                i+=1
                stdscr.addstr('toto is dead: '+str(i))
                stdscr.keypad(1)
            stdscr.addstr("\n\nPress b to go back")  
            
            while True:
                event2 = stdscr.getch()
                if event2 == ord("b"): 
                    stdscr.clear()
                    break
                    
        elif event == curses.KEY_DOWN:
            stdscr.clear()
            stdscr.addstr("The User Pressed DOWN")       
    stdscr.refresh()
    stdscr.getkey()

    
if __name__ == '__main__':
    #main()
    gmail(False)
    wrapper(prg)

