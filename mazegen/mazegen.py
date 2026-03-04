from typing import List
import random


class MazeGenerator:
    """
    Maze generator class using DFS algorithm.

    Attributes:
        direction: Dictionary mapping direction letters to (dx, dy) offsets.
        wall_bits: Dictionary mapping direction letters to wall bit values.
        opposite_direction: Dictionary mapping each direction to its opposite.
        width: Width of the maze.
        height: Height of the maze.
        grid: 2D list representing the maze cells with wall bits.
        visited: Set of visited cells during maze generation.
        visited_42: Set of cells belonging to the 42 pattern.
    """
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

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the maze generator with given width and height.
        """
        self.height: int = height
        self.width: int = width
        self.grid: List[List[int]] = []
        self.visited: set[tuple[int, int]] = set()
        self.visited_42: set[tuple[int, int]] = set()

    def maze(self) -> List[List[int]]:
        """
        Initialize a maze grid filled with all walls (value 15).

        Returns:
            The initialized grid as a 2D list of integers.
        """
        self.grid = []
        for _ in range(self.height):
            a = []
            for _ in range(self.width):
                a.append(15)
            self.grid.append(a)
        return self.grid

    def check_bounds(self, x: int, y: int) -> bool:
        """
        Check whether the given coordinates are inside the maze bounds.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            True if (x, y) is within the maze; False otherwise.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def remove_wall(self, x: int, y: int, wall_bit: int) -> None:
        """
        Remove a wall from a cell if it is not part of the 42 pattern.

        Args:
            x: Column index.
            y: Row index.
            wall_bit: Bit representing the wall to remove.
        """
        if self.check_bounds(x, y):
            if (x, y) not in self.visited_42:
                self.grid[y][x] &= ~wall_bit

    def get_neighbors(self, x: int, y: int) -> List[tuple[int, int]]:  # noqa
        """
        Get unvisited neighbors of a cell, ignoring cells in visited_42.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            A list of neighboring coordinates as (x, y) tuples.
        """
        nieghbors: List[tuple[int, int]] = []

        for _, (dx, dy) in self.direction.items():
            nx = x + dx
            ny = y + dy

            if self.check_bounds(nx, ny) and (nx, ny) not in self.visited and (nx, ny) not in self.visited_42:  # noqa
                nieghbors.append((nx, ny))

        return nieghbors

    def carve(self, x: int, y: int, nx: int, ny: int) -> None:
        """
        Carve a passage between two adjacent cells.

        Args:
            x: Current cell column.
            y: Current cell row.
            nx: Neighbor cell column.
            ny: Neighbor cell row.
        """
        dx = nx - x
        dy = ny - y

        for direction, (ddx, ddy) in self.direction.items():
            if ddx == dx and ddy == dy:
                wall = self.wall_bits[direction]
                opp_wall = self.wall_bits[self.opposite_direction[direction]]
                self.remove_wall(x, y, wall)
                self.remove_wall(nx, ny, opp_wall)
                break

    def make_imperfect(self, chance: float = 0.05) -> None:
        """
        Randomly remove walls to make the maze imperfect.

        Args:
            chance: Probability of removing a wall (default 0.05).
        """
        if self.width * self.height < 100:
            chance = 0.1
        for y in range(self.height):
            for x in range(self.width):
                for direction, (dx, dy) in self.direction.items():
                    nx = x + dx
                    ny = y + dy

                    if not self.check_bounds(nx, ny):
                        continue

                    if random.random() < chance:
                        wall = self.wall_bits[direction]
                        opposite = self.wall_bits[self.opposite_direction[direction]]  # noqa

                        self.remove_wall(x, y, wall)
                        self.remove_wall(nx, ny, opposite)


    def generate(self, entry: tuple[int, int], end: tuple[int, int], se: int | None, perfect: bool = True) -> List[List[int]] | None:  # noqa
        """
        Generate a maze using DFS and optionally make it imperfect.

        Args:
            entry: Entry coordinates (x, y).
            end: Exit coordinates (x, y).
            se: Optional random seed.
            perfect: Whether to generate a perfect maze.

        Returns:
            The generated maze grid, or None if entry/exit overlaps 42 pattern.
        """
        self.maze()
        self.visited = set()
        self.print_42()
        x, y = entry

        # swapped = {(x, y) for (y, x) in self.visited_42}
        if entry in self.visited_42 or end in self.visited_42:
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

    def print_42(self) -> None:
        """
        Carve the 42 pattern in the center of the maze and mark visited_42 cells. # noqa
        """
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
