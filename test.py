from typing import List
import curses


class test:
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.grid = List[List[str]]

    def mz(self):
        self.grid = []
        for _ in range(self.x):
            a = []
            for _ in range(self.y):
                a.append("0")
            self.grid.append(a)
        return self.grid


def display_maze(stdscr, grid):
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, "█")
                stdscr.attroff(curses.color_pair(1))

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(len(grid) + 1, 0, "Press 'q' to quit, 'r' to regenerate")
        stdscr.attroff(curses.color_pair(1))

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('r'):
            grid = test(10, 15).mz()
            continue


tt = test(30, 40)
a = tt.mz()

curses.wrapper(display_maze, a)
