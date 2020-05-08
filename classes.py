from utils import os, curses
import shutil

class File:
    def __init__(self, name):
        self.name = name

    def render(self, depth, width):
        return '{}{}'.format(' '*depth, os.path.basename(self.name))

    def traverse(self):
        yield self, 0

    def open(self, stdscr):
        curses.endwin()
        os.system('$EDITOR {}'.format(self.name))

    def delete(self, stdscr):
        os.remove(self.name)

    def rename(self, stdscr):
        new_name = user_input(stdscr, "Please, enter a new name")
        os.rename(self.name, '{}/{}'.format(os.path.dirname(self.name), new_name))
        self.name = '{}/{}'.format(os.path.dirname(self.name), new_name)

    def move(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        shutil.move(self.name, new_place)

    def copy(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        shutil.copyfile(self.name, new_place)

    def collapse(self, stdscr):
        pass

class Dir(File):
    def __init__(self, name):
        File.__init__(self, name)
        self.kids = [dir_or_file(os.path.join(self.name, kid)) for kid in sorted(os.listdir(name))]
        self.opened = False

    def render(self, depth, width):
        return '{}{}{}'.format(' '*depth, self.icon(), os.path.basename(self.name))

    def icon(self):
        if self.opened:
            return '[-]'
        elif self.kids is None:
            return '[?]'
        else:
            return '[+]'

    def open(self, stdscr):
        self.opened = True

    def delete(self, stdscr):
        shutil.rmtree(self.name)

    def rename(self, stdscr):
        new_name = user_input(stdscr, "Please, enter a new name")
        os.rename(self.name, '{}/{}'.format(os.path.dirname(self.name), new_name))
        self.name = '{}/{}'.format(os.path.dirname(self.name), new_name)

    def move(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        shutil.move(self.name, new_place)

    def copy(self, stdscr):
        new_place = user_input(stdscr, "Please, enter a path")
        shutil.copyfile(self.name, new_place)

    def collapse(self, stdscr):
        self.opened = False

    def traverse(self):
        yield self, 0
        if not self.opened:
            return
        for child in self.kids:
            for kid, depth in child.traverse():
                yield kid, depth + 1

def dir_or_file(name):
    if os.path.isdir(name):
        return Dir(name)
    else:
        return File(name)

def user_input(stdscr, help_msg):
    curses.endwin()
    height, width = stdscr.getmaxyx()
    inp = curses.newwin(height, width, 0,0)
    inp.attron(curses.color_pair(1))
    curses.curs_set(1)

    inp.addstr(1,1, help_msg)
    sub = inp.subwin(1, width-1, 3, 1)
    inp.refresh()
    tb = curses.textpad.Textbox(sub, insert_mode=True)
    return str(tb.edit().rstrip())