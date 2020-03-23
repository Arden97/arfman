import os
import sys
import curses
from curses import textpad

class File:
    def __init__(self, name):
        self.name = name

    def render(self, depth, width):
        return '{}{}'.format('   '*depth, os.path.basename(self.name))

    def traverse(self): 
        yield self, 0

    def open(self, stdscr):
        curses.endwin()
        os.system('$EDITOR {}'.format(self.name))

    def delete(self, stdscr):
        os.system('rm {}'.format(self.name))

    def rename(self, stdscr):
        new_name = user_input(stdscr, "Please, enter a new name") 
        os.rename(self.name, '{}/{}'.format(os.path.dirname(self.name), new_name))
        self.name = '{}/{}'.format(os.path.dirname(self.name), new_name)

    def move(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        os.system('mv {} {}'.format(self.name, new_place))

    def copy(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        os.system('cp {} {}'.format(self.name, new_place))

    def collapse(self, stdscr): 
        pass

class Dir(File):
    def __init__(self, name):
        File.__init__(self, name)
        self.kids = {k:v for k,v in zip(sorted(os.listdir(name)),
            [dir_or_file(os.path.join(self.name, kid)) for kid in sorted(os.listdir(name))])}
        self.opened = False

    def render(self, depth, width):
        return '{}{}{}'.format('   '*depth, self.icon(), os.path.basename(self.name))

    def icon(self):
        if self.opened:
            return '[-]'
        elif self.kids.keys() is None:
            return '[?]'
        else:
            return '[+]'

    def open(self, stdscr): 
        self.opened = True

    def delete(self, stdscr):
        os.system('rm -rf {}'.format(self.name))

    def rename(self, stdscr):
        new_name = user_input(stdscr, "Please, enter a new name") 
        os.rename(self.name, '{}/{}'.format(os.path.dirname(self.name), new_name))
        self.name = '{}/{}'.format(os.path.dirname(self.name), new_name)

    def move(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        os.system('mv {} {}'.format(self.name, new_place))

    def copy(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        os.system('cp {} {}'.format(self.name, new_place))
        
    def collapse(self, stdscr): 
        self.opened = False

    def traverse(self):
        yield self, 0
        if not self.opened:
            return
        for child in self.kids.values():
            for kid, depth in child.traverse():
                yield kid, depth + 1

def dir_or_file(name):
    if os.path.isdir(name): 
        return Dir(name)
    else: 
        return File(name)

# TODO: cancel input
def user_input(stdscr, help_msg):
    curses.endwin()
    height, width = stdscr.getmaxyx()
    inp = curses.newwin(height, width, 0,0)
    inp.attron(curses.color_pair(1))
    inp.addstr(1,1, help_msg)
    sub = inp.subwin(height-3, width-1, 3, 1)
    inp.refresh()
    tb = curses.textpad.Textbox(sub, insert_mode=True)
    return str(tb.edit().rstrip())

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

def process_files(stdscr, item):
    curidx = 0 # cursor's line number
    pending_action = None

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        line = 0
        
        # To avoid errors when deleting an item during iteration, list() is used
        # TODO: Is there more elegant way to do this?
        for data, depth in list(item.traverse()):
            if line == curidx:
                stdscr.attrset(curses.color_pair(1) | curses.A_BOLD)
                if pending_action:
                    getattr(data, pending_action)(stdscr)
                    if(pending_action == 'delete' or pending_action == 'move'):
                        del item.kids[os.path.basename(data.name)]
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
        elif ch == ord('d'):
            pending_action = 'delete'
        elif ch == ord('r'):
            pending_action = 'rename'
        elif ch == ord('c'):
            pending_action = 'copy'
        elif ch == ord('m'):
            pending_action = 'move'
        elif ch == curses.KEY_PPAGE:
            curidx -= height
            if curidx < 0:
                curidx = 0
        elif ch == curses.KEY_NPAGE:
            curidx += height
            if curidx >= line: 
                curidx = line - 1
        elif ch == ord('q'):
            return

        curidx %= line