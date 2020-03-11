import os
import sys
import curses

class File:
    def __init__(self, name):
        self.name = name

    def render(self, depth, width):
        return '{}{}'.format('   '*depth, os.path.basename(self.name))

    def traverse(self): 
        yield self, 0

    def open(self):
        curses.endwin()
        os.system('nvim {}'.format(self.name))

    def delete(self):
        #TODO screen is not updating after delete command
        os.system('rm {}'.format(self.name))

    def rename(self):
        pass
        # new_name = 'New name'
        # os.system('mv {} {}'.format(self.name, new_name))

    def move(self):
        pass
        # new_place = ''
        # os.system('mv {} {}'.format(self.name, new_place))

    def copy(self):
        pass
        # new_place = ''
        # os.system('cp {} {}'.format(self.name, new_place))

    def collapse(self): 
        pass

class Dir(File):
    def __init__(self, name):
        File.__init__(self, name)
        self.kids = {k:v for k,v in zip(sorted(os.listdir(name)),
            [dir_or_file(os.path.join(self.name, kid)) for kid in sorted(os.listdir(name))] )}
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

    def open(self): 
        self.opened = True

    def delete(self):
        os.system('rm -rf {}'.format(self.name))

    def rename(self):
        pass
        # new_name = 'New name'
        # os.system('mv {} {}'.format(self.name, new_name))

    def move(self):
        pass
        # new_place = ''
        # os.system('mv {} {}'.format(self.name, new_place))

    def copy(self):
        pass
        # new_place = ''
        # os.system('cp {} {}'.format(self.name, new_place))
        
    def collapse(self): 
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

        for data, depth in item.traverse():
            if line == curidx:
                stdscr.attrset(curses.color_pair(1) | curses.A_BOLD)
                if pending_action:
                    getattr(data, pending_action)()
                    pending_action = None
                    stdscr.refresh()
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