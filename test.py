from typing import List
import sys
import curses
import random
from config import pars_config


class test:
    direction = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }

    wall_bits = {
        'N': 1,
        'E': 2,
        'S': 4,
        'W': 8
    }

    opposite_direction = {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E'
    }

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.grid: List[List[int]] = []

    def mz(self):
        self.grid = []
        for _ in range(self.height):
            a = []
            for _ in range(self.width):
                a.append(15)
            self.grid.append(a)
        return self.grid

    # TODO -> hnaya kanchof yak ma position kharja bra grid
    def check_bounds(self, col, row):
        if 0 <= col < self.width and 0 <= row < self.height:
            return True
        return False

    def remove_wall(self, col, row, wall_bit: int) -> None:
        if self.check_bounds(col, row):
            self.grid[row][col] &= ~wall_bit

    # TODO -> hnaya kn9lb 3la neighbors o kanchof wach visited olala
    def get_neighbors(self, col: int, row: int, visited: set) -> List[tuple[int, int]]: # noqa
        nieghbors = []

        for _, (dx, dy) in self.direction.items():
            nx = col + dx
            ny = row + dy
            # TODO -> hnaya kanchof N, S, E, W li i9der idoz lihom
            if self.check_bounds(nx, ny) and (nx, ny) not in visited:
                nieghbors.append((nx, ny))

        return nieghbors

    def carve(self, col: int, row: int, nx: int, ny: int) -> None:
        dx = nx - col
        dy = ny - row

        for direction, (ddx, ddy) in self.direction.items():
            if ddx == dx and ddy == dy:
                wall = self.wall_bits[direction]
                opp_wall = self.wall_bits[self.opposite_direction[direction]]
                self.remove_wall(col, row, wall)
                self.remove_wall(nx, ny, opp_wall)
                break

    def generate(self, entry: tuple[int, int], se: int | None) -> List[List[int]]: # noqa
        self.mz()
        stack = [entry]
        visited = {entry}

        if se is not None:
            random.seed(se)
        else:
            random.seed(None)
        while stack:
            col, row = stack[-1]
            neighbors = self.get_neighbors(col, row, visited)
            if neighbors:
                next_col, next_row = random.choice(neighbors)
                self.carve(col, row, next_col, next_row)
                visited.add((next_col, next_row))
                stack.append((next_col, next_row))
            else:
                stack.pop()
        return self.grid


def print_maze(stdscr, generator, width, height, data):
    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

    color_index = 1
    show_color_menu = False

    while True:
        stdscr.clear()

        if show_color_menu:
            stdscr.addstr(0, 0, "=== Choose Color ===", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(3)) # noqa
            stdscr.addstr(1, 0, "1. WHITE", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(2, 0, "2. CYAN", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(3, 0, "3. GREEN", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(4, 0, "4. MAGENTA", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(5, 0, "5. RED", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(6, 0, "6. YELLOW", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(7, 0, "7. BLUE", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa

        else:
            grid = generator.grid

            for row in range(height):

                top_line = ""
                for col in range(width):
                    cell = grid[row][col]
                    top_line += "███" if cell & 1 else "█  "
                top_line += "█"
                stdscr.addstr(row * 2, 0, top_line, curses.color_pair(color_index)) # noqa

                west_line = ""
                for col in range(width):
                    cell = grid[row][col]
                    west_line += "█  " if cell & 8 else "   "
                west_line += "█"
                stdscr.addstr(row * 2 + 1, 0, west_line, curses.color_pair(color_index)) # noqa

            stdscr.addstr(height * 2, 0, "█" + "███" * width, curses.color_pair(color_index)) # noqa

            stdscr.addstr(height * 2 + 2, 0, "=== A-Maze-ing ===", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(3)) # noqa
            stdscr.addstr(height * 2 + 3, 0, "1. Re-generate a new maze", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(height * 2 + 4, 0, "2. Show/Hide path from entry to exit", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(height * 2 + 5, 0, "3. Rotate maze colors", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa
            stdscr.addstr(height * 2 + 6, 0, "4. Quit", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1)) # noqa

        stdscr.refresh()
        key = stdscr.getch()

        if show_color_menu:
            if key == ord("1"):
                color_index = 1
                show_color_menu = False
            if key == ord("2"):
                color_index = 2
                show_color_menu = False
            if key == ord("3"):
                color_index = 3
                show_color_menu = False
            if key == ord("4"):
                color_index = 4
                show_color_menu = False
            if key == ord("5"):
                color_index = 5
                show_color_menu = False
            if key == ord("6"):
                color_index = 6
                show_color_menu = False
            if key == ord("7"):
                color_index = 7
                show_color_menu = False
        else:
            if key == ord("1"):
                generator.generate(data.entry, data.seed)

            if key == ord("3"):
                show_color_menu = True

                # color_index = (color_index % 7) + 1
            if key == ord("4"):
                break


def main(argv):
    if len(argv) != 2:
        print("ERROR: usage: python3 a_maze_ing.py config.txt")
        return None
    try:
        file = argv[-1]
        data = pars_config(file)
        if data is None:
            return None

        tt = test(data.width, data.height)
        tt.generate((data.entry), data.seed)

        curses.wrapper(print_maze, tt, data.width, data.height, data)
    except Exception as error:
        print(f"ERROR: {error}")
        return None


main(sys.argv)
