import curses
from curses import wrapper

def printTerminal(text,object,header=False):
    lenText = len(text)+4
    if header: object.addstr('#'*lenText+'\n')
    if header:
        borderLeft = '# '
        borderRight = ' #'
    else:
        borderLeft = ''
        borderRight = ''
    object.addstr(borderLeft+text+borderRight+'\n')
    if header: object.addstr('#'*lenText+'\n')



def prg(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(2, 11):
        v = i-1
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    #stdscr.addstr("Fisher Price Chatter\n\n")
    #stdscr.addstr("1] Read Enzo emails\n")
    #stdscr.addstr("2] Print hello world!\n")
    
    
    menu = ["Fisher Price Chatter\n\n","1] Read Enzo emails\n","2] Print hello world!\n"]

    while True:
        for iMenu in menu:
            stdscr.addstr(iMenu)
        event = stdscr.getch()
        if event == ord("q"): break
        elif event ==  ord("1"):
            stdscr.clear()
            #gmail(stdscr)
            printTerminal("You have [4] messages",stdscr,True)
            #stdscr.keypad(1)
        elif event ==  ord("2"):
            stdscr.clear()
            printTerminal("You have [4] messages",stdscr,False)
            stdscr.addstr("The User Pressed 2")
            #stdscr.keypad(1)
        #elif event == curses.KEY_UP:
        elif event == ord("3"):
            stdscr.clear()
            stdscr.addstr("The User Pressed UP")
            stdscr.clear()
            #stdscr.clear()
            for ind in range(1,100):
                #stdscr.addstr(ind, 0, 'toto is dead {}'.format(ind))
                print('\ntoto is dead {}'.format(ind))
                #stdscr.clear()
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
    #gmail(False)
    wrapper(prg)
