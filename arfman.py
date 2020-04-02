#!/usr/bin/python
from utils import *

#TODO status bar?
#TODO new file

def main(stdscr):
    init_colors()
    screen_routine(stdscr)
    start_dir = os.getcwd()
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]

    item = Dir(start_dir)
    item.open(stdscr)
    
    process_files(stdscr, item)

if __name__ == '__main__':
    curses.wrapper(main) 