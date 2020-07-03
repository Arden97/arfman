import sys
from classes import *
from curses import textpad

def help(stdscr):
    curses.endwin()
    height, width = stdscr.getmaxyx()
    win = curses.newwin(height, width, 0,0)
    win.attron(curses.color_pair(1))
    curses.curs_set(0)

    while True:
        win.addstr(0,0, "[UP_ARROW][DOWN_ARROW] - navigation")
        win.addstr(1,0, "[LEFT_ARROW][RIGHT_ARROW] - collapse/open")
        win.addstr(2,0, "[c] - copy")
        win.addstr(3,0, "[d] - delete")
        win.addstr(4,0, "[m] - move")
        win.addstr(5,0, "[r] - rename")
        win.addstr(6,0, "[n] - new file")
        win.addstr(7,0, "[d] - new directory")
        win.addstr(8,0, "[g]- go to directory")
        win.addstr(9,0, "[q] - quit")
        win.addstr(11,0, "PRESS q TO GO BACK")
        win.refresh()
        if stdscr.getch() == ord('q'):
            return

def screen_routine(win):
    win.clear()
    win.refresh()
    curses.nl()
    curses.noecho()
    win.timeout(0)
    win.nodelay(0)

def init_colors():
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)

def new_file(root, stdscr):
    name = user_input(stdscr, "Please, enter a new file name")
    root.kids.append(File(name))
    root.kids = sorted(root.kids)
    os.system('touch {}'.format(name))

def new_dir(root, stdscr):
    name = user_input(stdscr, "Please, enter a new folder name")
    os.system('mkdir {}'.format(name))
    root.kids.append(Dir(name))

def go_to_dir(stdscr):
    path = user_input(stdscr, "Please, enter a path")
    return Dir(path)

def process_files(stdscr, root):
    curidx = 0 # cursor line number
    pending_action = None
    ignore = []

    while True:
        curses.curs_set(0)
        stdscr.clear()
        _, width = stdscr.getmaxyx()
        line = 0

        for data, depth in root.traverse():
            if data.name in ignore:
                continue
            if line == curidx:
                stdscr.attrset(curses.color_pair(1) | curses.A_BOLD)
                if pending_action:
                    getattr(data, pending_action)(stdscr)
                    if pending_action == 'delete' or pending_action == 'move':
                        ignore.append(data.name)
                        pending_action = None
                        continue
                    else: 
                        pending_action = None
            else:
                stdscr.attrset(curses.color_pair(1))
            stdscr.addstr(line, 0, data.render(depth, width))
            line += 1

        # stdscr.addstr(line+1, 0, "Press h for help.")
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
            if curidx == 0: # ignore root of tree
                continue
            pending_action = 'delete'
        elif ch == ord('m'):
            pending_action = 'move'
        elif ch == ord('r'):
            pending_action = 'rename'
        elif ch == ord('n'):
            new_file(root, stdscr)
        elif ch == ord('f'):
            new_dir(root, stdscr)
        elif ch == ord('g'):
            root = go_to_dir(stdscr)
            root.open(stdscr)
        elif ch == ord('h'):
            help(stdscr)
        elif ch == ord('q'):
            return

        curidx %= line