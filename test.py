from typing import List
import curses
import random


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
        self.grid: List[List[str]] = []

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
    def get_neighbors(self, col: int, row: int, visited: set) -> List[tuple[int, int]]:
        nieghbors = []

        for direction, (dx, dy), in self.direction.items():
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

    def generate(self, entry: tuple[int, int]) -> List[List[int]]:
        self.mz()
        stack = [entry]
        visited = {entry}

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


def print_maze(grid, width, height):
    """Print maze as ASCII art."""
    for row in range(height):
        # top walls
        line = ""
        for col in range(width):
            cell = grid[row][col]
            line += "+--" if cell & 1 else "+  "
        line += "+"
        print(line)

        # west walls
        line = ""
        for col in range(width):
            cell = grid[row][col]
            line += "|  " if cell & 8 else "   "
        line += "|"
        print(line)

    # bottom border
    print("+" + "--+" * width)


tt = test(10, 10)
grid = tt.generate((0, 0))
print_maze(grid, 10, 10)


# def display_maze(stdscr, grid):
#     curses.curs_set(0)

#     curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

#     while True:
#         stdscr.clear()

#         for y, row in enumerate(grid):
#             for x, cell in enumerate(row):
#                 stdscr.attron(curses.color_pair(1))
#                 stdscr.addstr(y, x, "█")
#                 stdscr.attroff(curses.color_pair(1))

#         stdscr.attron(curses.color_pair(1))
#         stdscr.addstr(len(grid) + 1, 0, "Press 'q' to quit, 'r' to regenerate")
#         stdscr.attroff(curses.color_pair(1))

#         stdscr.refresh()

#         key = stdscr.getch()

#         if key == ord('q'):
#             break
#         elif key == ord('r'):
#             grid = test(10, 15).mz()
#             continue


# tt = test(10, 20)
# a = tt.mz()

# curses.wrapper(display_maze, a)
