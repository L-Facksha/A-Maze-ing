from typing import List
import random


class MazeGenerator:
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
        self.visited_42: set = set()

    def maze(self):
        self.grid = []
        for _ in range(self.height):
            a = []
            for _ in range(self.width):
                a.append(15)
            self.grid.append(a)
        return self.grid

    def check_bounds(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def remove_wall(self, x, y, wall_bit: int) -> None:
        if self.check_bounds(x, y):
            if (x, y) not in self.visited_42:
                self.grid[y][x] &= ~wall_bit

    def get_neighbors(self, x: int, y: int) -> List[tuple[int, int]]:  # noqa
        nieghbors = []

        for _, (dx, dy) in self.direction.items():
            nx = x + dx
            ny = y + dy

            if self.check_bounds(nx, ny) and (nx, ny) not in self.visited and (nx, ny) not in self.visited_42: # noqa
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
        if self.width * self.height < 100:
            chance = 0.3
        for y in range(self.height):
            for x in range(self.width):
                for direction, (dx, dy) in self.direction.items():
                    nx = x + dx
                    ny = y + dy

                    if not self.check_bounds(nx, ny):
                        continue

                    if random.random() < chance:
                        wall = self.wall_bits[direction]
                        opposite = self.wall_bits[self.opposite_direction[direction]] # noqa

                        self.remove_wall(x, y, wall)
                        self.remove_wall(nx, ny, opposite)

    def generate(self, entry: tuple[int, int], end: tuple[int, int], se: int | None, perfect: bool = True) -> List[List[int]]:  # noqa
        self.maze()
        self.visited = set()
        self.print_42()
        y, x = entry

        swapped = {(x, y) for (y, x) in self.visited_42}
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
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        patteren_height = len(set_42)
        patteren_width = len(set_42[0])

        if self.width <= patteren_width or self.height <= patteren_height:
            return

        if not self.grid:
            self.maze()

        x = max((self.width - patteren_width) // 2, 0)
        y = max((self.height - patteren_height) // 2, 0)
        for r in set_42:
            col = x
            for c in r:
                if c == 1:
                    self.grid[y][col] = 15
                    self.visited_42.add((col, y))
                col += 1
            y += 1
