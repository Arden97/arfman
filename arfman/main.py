#!/usr/bin/python
from .utils import *

def main():
    stdscr = init_screen()
    init_colors()
    start_dir = os.getcwd()
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    root = Dir(start_dir)
    root.open(stdscr)
    process_files(stdscr, root)
    end_screen(stdscr)