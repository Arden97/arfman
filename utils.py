import os
import sys
import curses
from curses import textpad
from classes import File, Dir, dir_or_file, user_input

def screen_routine(win):
    win.clear()
    win.refresh()
    curses.nl()
    curses.noecho()
    curses.curs_set(0)
    win.timeout(0)
    win.nodelay(0)

def init_colors():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)

def new_file(item, stdscr):
    name = user_input(stdscr, "Please, enter a new file name")
    item.kids.append(File(name))
    item.kids = sorted(item.kids)
    os.system('touch {}'.format(name))

def new_dir(item, stdscr):
    name = user_input(stdscr, "Please, enter a new folder name")
    os.system('mkdir {}'.format(name))
    item.kids.append(Dir(name))
    item.kids = sorted(item.kids)

def go_to_dir(stdscr):
    path = user_input(stdscr, "Please, enter a new place path")
    return Dir(path)

def process_files(stdscr, item):
    curidx = 0 # cursor line number
    pending_action = None
    ignore = []

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        line = 0

        for data, depth in item.traverse():
            if data.name in ignore:
                continue
            if line == curidx:
                stdscr.attrset(curses.color_pair(1) | curses.A_BOLD)
                if pending_action:
                    getattr(data, pending_action)(stdscr)
                    if(pending_action == 'delete' or pending_action == 'move'):
                        ignore.append(data.name)
                        pending_action = None
                        continue
                    else: 
                        pending_action = None
            else:
                stdscr.attrset(curses.color_pair(1))
            stdscr.addstr(line, 0, data.render(depth, width))
            line += 1

        stdscr.refresh()

        ch = stdscr.getch()
        if ch == curses.KEY_UP: 
            curidx -= 1
        elif ch == curses.KEY_DOWN:
            curidx += 1
        elif ch == curses.KEY_RIGHT:
            pending_action = 'open'
        elif ch == curses.KEY_LEFT:
            pending_action = 'collapse'
        elif ch == ord('c'):
            pending_action = 'copy'
        elif ch == ord('d'):
            pending_action = 'delete'
        elif ch == ord('m'):
            pending_action = 'move'
        elif ch == ord('r'):
            pending_action = 'rename'
        elif ch == ord('n'):
            new_file(item, stdscr)
        elif ch == ord('f'):
            new_dir(item, stdscr)
        elif ch == ord('g'):
            item = go_to_dir(stdscr)
        elif ch == ord('q'):
            return

        curidx %= line