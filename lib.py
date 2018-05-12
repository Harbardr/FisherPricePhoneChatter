#! /usr/lib/python

def asciiCar(stdscr):
    stdscr.addstr("          _____________________\n")
    stdscr.addstr("         //~~~~~~~~~~~~~~~~~~~\\\\\n")
    stdscr.addstr("        //                     \\\\\n")
    stdscr.addstr("       //_______________________\\\\\n")
    stdscr.addstr("     /  /                       \\  \\\n")
    stdscr.addstr("    /  /                         \\  \\\n")
    stdscr.addstr("   /__/___________________________\\__\\\n")
    stdscr.addstr("  |/| ____ ||||||||||||||||||| ____ |\\|\n")
    stdscr.addstr("  |/|______|||||||DODGE|||||||______|\\|\n")
    stdscr.addstr("  |/ ||  |||||||||||||||||||||||  || \\|\n")
    stdscr.addstr(" /-------------------------------------\\\n")
    stdscr.addstr("  ------------------------------------- \n")
    stdscr.addstr("  |\\_________________________________/|\n")
    stdscr.addstr("  |     |                       |     |\n")
    stdscr.addstr("  |_____|                       |_____|\n")



def todayDate():
    say(dico["DATE"].format(CHATTER_DATE_TODAY),CHATTER_LANG)