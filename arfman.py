#!/usr/bin/python
from utils import *

#TODO goto autofill ?
#TODO sort files?
#TODO show/hide dotfiles
#TODO replace
#TODO copy directory

def main(stdscr):
    init_colors()
    screen_routine(stdscr)
    start_dir = os.getcwd()
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]

    root = Dir(start_dir)
    root.open(stdscr)

    process_files(stdscr, root)

if __name__ == '__main__':
    curses.wrapper(main)