from config import pars_config
from mazegen import MazeGenerator
from display import print_maze
import curses
import sys
from mazegen import bfs
from m_to_hex import m_to_hex


def main(argv):
    if len(argv) != 2:
        print("ERROR: usage: python3 a_maze_ing.py config.txt")
        return None
    # try:
    file = argv[-1]
    data = pars_config(file)
    if data is None:
        return None

    grid = MazeGenerator(data.width, data.height)
    grid.maze()
    grid.print_42()

    result = grid.generate((data.entry), data.exit1, data.seed, data.perfect) # noqa

    if result is None:
        print("ERROR: ENTRY or EXIT overlaps 42 patteren")
        return None

    path = bfs(grid.grid, data.entry, data.exit1, data.width, data.height)
    m_to_hex(result, data.entry, data.exit1, data.width, data.height, path)

    curses.wrapper(print_maze, grid, data.width, data.height, data, path, grid.visited_42) # noqa

    # except Exception as error:
    #     print(f"ERROR: {error}")
    #     return None


main(sys.argv)
