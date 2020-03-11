#!/usr/bin/python
from utils import *

#TODO find the way to make user input visible in a new window
#TODO status bar?
#TODO it's kind of slow

def main(stdscr):
    init_colors()
    screen_routine(stdscr)
    start_dir = os.getcwd()
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    item = Dir(start_dir)
    item.open()
    # act_bar = "[d] - delete [r] - rename [m] - move [c] - copy [q] - quit"

    process_files(stdscr, item)

if __name__ == '__main__':
    curses.wrapper(main) 