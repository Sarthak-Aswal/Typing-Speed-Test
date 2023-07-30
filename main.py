import curses
from curses import wrapper
import random
import time

#displays the start message at the beginning
def start(stdscr):
     stdscr.clear()
     stdscr.addstr("Hello user,do you want to know your typing speed?\n")
     stdscr.addstr("Press enter to continue")
     stdscr.refresh()
     stdscr.getkey()

#loads the target text from a text file
def loadtarget():
    with open("targets.txt",'r') as tr:
        lines=tr.readlines()
        #selects and returns a random line from list of lines and removes trailing space and \n
        return random.choice(lines).strip()

#displays the rules
def rules(stdscr):
    stdscr.clear()
    stdscr.addstr("Rules:\n")
    stdscr.addstr("1)Press esc to exit the test anytime you want")
    stdscr.addstr("\n2)Complete the given target text to know your wpm")
    stdscr.addstr("\n3)Press any key to start the test")
    stdscr.refresh()
    stdscr.getkey()

#the main typing test
def typingtest(stdscr):
     target=loadtarget()
     current=[]
     wpm=0
     starttime=time.time()
     stdscr.nodelay(True)
     while True:
        time_elapsed = max(time.time() - starttime, 1)
        wpm = round((len(current) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        stdscr.addstr(target)
        stdscr.addstr(2,0,f"Wpm:{wpm}")

        for i, char in enumerate(current):#displays green or red currently entered text over target text
            color = curses.color_pair(2)#green text if text is correct
            if current[i] != target[i]:
                color = curses.color_pair(3)#red text if text is incorrect

            stdscr.addstr(0, i, char, color)
        stdscr.refresh()

        #checks if user completed the test and break if completed
        if "".join(current) == target:
            stdscr.nodelay(False)
            break

	    #gets the text from user
        try:
            key=stdscr.getkey()
        except:
            continue
        #if user entered esc exit the program
        if ord(key) == 27:
            break

        #if user entered backspace delete the text from current list
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current)>0:
                current.pop()

        #append the user entered text if length is not equal to target string
        elif len(current)!=len(target):
            current.append(key)
        else:
            continue

        stdscr.refresh()

#main function    
def main(stdscr):
     curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
     curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
     curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
     start(stdscr)
     rules(stdscr)
     while(True):
         typingtest(stdscr)
         stdscr.addstr(3,0,"You have completed the test press enter to continue or esc to exit")
         key=stdscr.getkey()
         if ord(key)==27:
             break
     
wrapper(main)