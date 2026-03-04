from mazegen.config import pars_config
from mazegen.mazegen import MazeGenerator
from mazegen.display import print_maze
from mazegen.bfs import bfs
from mazegen.m_to_hex import m_to_hex
import curses
import sys


def main(argv: list[str]) -> None:
    """
    Entry point of the maze generator program.

    Reads a configuration file, generates a maze (with optional 42 pattern),
    solves it, and outputs both a hexadecimal representation and an ASCII
    visualisation.

    Args:
        argv (list[str]): Command-line arguments (should contain the config file path). # noqa

    Returns:
        None

    Any errors (e.g., missing config file, invalid parameters) are caught and
    printed; the program then exits gracefully.
    """
    if len(argv) != 2:
        print("ERROR: usage: python3 a_maze_ing.py config.txt")
        return None
    try:
        file = argv[-1]
        data = pars_config(file)
        if data is None:
            return None

        grid = MazeGenerator(data.width, data.height)
        grid.maze()
        grid.print_42()

        result = grid.generate(data.entry, data.exit1, data.seed, data.perfect)  # noqa

        if result is None:
            print("ERROR: ENTRY or EXIT overlaps 42 patteren")
            return None

        path = bfs(grid.grid, data.entry, data.exit1, data.width, data.height)
        if not path:
            print("ERROR: this maze has no way to be solved!")
            return None
        m_to_hex(result, data.entry, data.exit1, data.width, data.height, path, data.output_file) # noqa

        curses.wrapper(print_maze, grid, data.width, data.height, data, path, grid.visited_42)  # noqa

    except Exception as error:
        print(f"ERROR: {error}")
        return None


if __name__ == "__main__":
    main(sys.argv)
