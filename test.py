from typing import List
import sys
import curses
import random
import bfs
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
        self.visited: set = set()

    def mz(self):
        self.grid = []
        for _ in range(self.height):
            a = []
            for _ in range(self.width):
                a.append(15)
            self.grid.append(a)
        return self.grid

    # TODO -> hnaya kanchof yak ma position kharja bra grid
    def check_bounds(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def remove_wall(self, x, y, wall_bit: int) -> None:
        if self.check_bounds(x, y):
            self.grid[y][x] &= ~wall_bit

    # TODO -> hnaya kn9lb 3la neighbors o kanchof wach visited olala
    def get_neighbors(self, x: int, y: int) -> List[tuple[int, int]]:  # noqa
        nieghbors = []

        for _, (dx, dy) in self.direction.items():
            nx = x + dx
            ny = y + dy
            # TODO -> hnaya kanchof N, S, E, W li i9der idoz lihom
            if self.check_bounds(nx, ny) and (nx, ny) not in self.visited:
                nieghbors.append((nx, ny))

        return nieghbors

    def carve(self, x: int, y: int, nx: int, ny: int) -> None:
        dx = nx - x
        dy = ny - y

        for direction, (ddx, ddy) in self.direction.items():
            if ddx == dx and ddy == dy:
                wall = self.wall_bits[direction]
                opp_wall = self.wall_bits[self.opposite_direction[direction]]
                self.remove_wall(x, y, wall)
                self.remove_wall(nx, ny, opp_wall)
                break

    def make_imperfect(self, chance=0.05):
        for y in range(self.height):
            for x in range(self.width):
                for direction, (dx, dy) in self.direction.items():
                    nx = x + dx
                    ny = y + dy

                    # only if inside grid
                    if not self.check_bounds(nx, ny):
                        continue

                    # remove wall randomly
                    if random.random() < chance:
                        wall = self.wall_bits[direction]
                        opposite = self.wall_bits[self.opposite_direction[direction]]

                        self.remove_wall(x, y, wall)
                        self.remove_wall(nx, ny, opposite)

    def generate(self, entry: tuple[int, int], end: tuple[int, int], se: int | None, perfect: bool = True) -> List[List[int]]:  # noqa
        self.mz()
        self.visited = set()
        self.print_42()
        y, x = entry
        ye, xe = end
        print(entry)
        swapped = {(x, y) for (y, x) in self.visited}
        if entry in swapped or end in swapped:
            return None
        stack = [entry]
        self.visited.add(entry)

        if se is not None:
            random.seed(se)
        else:
            random.seed(None)
        while stack:
            x, y = stack[-1]
            neighbors = self.get_neighbors(x, y)
            if neighbors:
                next_x, next_y = random.choice(neighbors)
                self.carve(x, y, next_x, next_y)
                self.visited.add((next_x, next_y))
                stack.append((next_x, next_y))
            else:
                stack.pop()
        if not perfect:
            self.make_imperfect(0.05)
        return self.grid

    def print_42(self):
        set_42 = [
            [1, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 1, 0]
        ]

        patteren_height = len(set_42)
        patteren_width = len(set_42[0])

        if self.width < patteren_width or self.height < patteren_height:
            print("ERROR: maze too small to display 42 pattern")
            return

        if not self.grid:
            self.mz()

        x = max((self.width - patteren_width) // 2, 0)
        y = max((self.height - patteren_height) // 2, 0)
        for r in set_42:
            col = x
            for c in r:
                if c == 1:
                    self.grid[y][col] = 15
                    self.visited.add((col, y))
                col += 1
            y += 1
        print(self.visited)

    def print_maze(self, stdscr, generator, width, height, data, path):
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
        path_show = False

        while True:
            stdscr.clear()

            if show_color_menu:
                stdscr.addstr(0, 0, "=== Choose Color ===", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(3))  # noqa
                stdscr.addstr(1, 0, "1. WHITE", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(2, 0, "2. CYAN", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(3, 0, "3. GREEN", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(4, 0, "4. MAGENTA", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(5, 0, "5. RED", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(6, 0, "6. YELLOW", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(7, 0, "7. BLUE", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa

            else:
                grid = generator.grid

                for y in range(height):

                    top_line = ""
                    for x in range(width):
                        cell = grid[y][x]
                        top_line += "███" if cell & 1 else "█  "
                    top_line += "█"
                    stdscr.addstr(y * 2, 0, top_line, curses.color_pair(color_index))  # noqa

                    west_line = ""
                    for x in range(width):
                        cell = grid[y][x]
                        west_line += "█  " if cell & 8 else "   "
                    west_line += "█"
                    stdscr.addstr(y * 2 + 1, 0, west_line, curses.color_pair(color_index))  # noqa

                stdscr.addstr(height * 2, 0, "█" + "███" * width, curses.color_pair(color_index))  # noqa

                stdscr.addstr(height * 2 + 2, 0, "=== A-Maze-ing ===", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(3))  # noqa
                stdscr.addstr(height * 2 + 3, 0, "1. Re-generate a new maze", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(height * 2 + 4, 0, "2. Show/Hide path from entry to exit", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(height * 2 + 5, 0, "3. Rotate maze colors", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                stdscr.addstr(height * 2 + 6, 0, "4. Quit", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(1))  # noqa
                if path_show:
                    for y, x in path:
                        stdscr.addstr(y * 2 + 1, x * 3 + 1, "•",
                                      curses.color_pair(5) | curses.A_BOLD)

                sy, sx = data.entry
                stdscr.addstr(sy * 2 + 1, sx * 3 + 1, "S",
                              curses.color_pair(3) | curses.A_BOLD)

                ey, ex = data.exit1
                stdscr.addstr(ey * 2 + 1, ex * 3 + 1, "E",
                              curses.color_pair(5) | curses.A_BOLD)

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
                    generator.generate(data.entry, data.exit1, data.seed, data.perfect)
                    path = bfs.bfs(generator.grid, data.entry, data.exit1)

                if key == ord("2"):
                    path_show = not path_show

                if key == ord("3"):
                    show_color_menu = True

                if key == ord("4"):
                    break


def main(argv):
    if len(argv) != 2:
        print("ERROR: usage: python3 a_maze_ing.py config.txt")
        return None
    # try:
    file = argv[-1]
    data = pars_config(file)
    if data is None:
        return None

    grid = test(data.width, data.height)

    result = grid.generate((data.entry), data.exit1, data.seed, data.perfect)
    print(result)
    if result is None:
        print("ERROR: ENTRY or EXIT overlaps 42 patteren")
        return None

    path = bfs.bfs(grid.grid, data.entry, data.exit1)

    curses.wrapper(grid.print_maze, grid, data.width, data.height, data, path)
    # print(path)
    # except Exception as error:
    #     print(f"ERROR: {error}")
    #     return None


main(sys.argv)
