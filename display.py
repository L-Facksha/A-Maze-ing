import curses
from mazegen import bfs
from m_to_hex import m_to_hex
import time


def print_maze(stdscr, generator, width, height, data, path, visited_42):
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
            stdscr.addstr(2, 0, "2. CYAN", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(2))  # noqa
            stdscr.addstr(3, 0, "3. GREEN", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(3))  # noqa
            stdscr.addstr(4, 0, "4. MAGENTA", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(4))  # noqa
            stdscr.addstr(5, 0, "5. RED", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(5))  # noqa
            stdscr.addstr(6, 0, "6. BLUE", curses.A_ITALIC | curses.A_BOLD | curses.color_pair(7))  # noqa

        else:
            if not generator.visited_42:
                stdscr.addstr(height * 2 + 7, 0, "WARNING: maze too small for 42 pattern", curses.color_pair(5) | curses.A_BOLD) # noqa
            grid = generator.grid

            for y in range(height):

                top_line = ""
                for x in range(width):
                    cell = grid[y][x]
                    top_line += "███" if cell & 1 else "█  "
                top_line += "█"
                stdscr.addstr(y * 2, 0, top_line, curses.color_pair(color_index))  # noqa

                for x in range(width):
                    if (x, y) in visited_42:
                        stdscr.addstr(y * 2, x * 3, "███",
                                      curses.color_pair(6))

                west_line = ""
                for x in range(width):
                    cell = grid[y][x]
                    west_line += "█  " if cell & 8 else "   "
                west_line += "█"
                stdscr.addstr(y * 2 + 1, 0, west_line, curses.color_pair(color_index))  # noqa

                for x in range(width):
                    if (x, y) in visited_42:
                        stdscr.addstr(y * 2 + 1, x * 3, "███",
                                      curses.color_pair(6))

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
                time.sleep(0.05)

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
                color_index = 7
                show_color_menu = False
        else:
            if key == ord("1"):
                generator.generate(data.entry, data.exit1,
                                   data.seed, data.perfect)
                path = bfs(generator.grid, data.entry,
                           data.exit1, data.width, data.height)
                time.sleep(0.05)
                m_to_hex(generator.grid, data.entry, data.exit1,
                         data.width, data.height, path)

            if key == ord("2"):
                path_show = not path_show

            if key == ord("3"):
                show_color_menu = True

            if key == ord("4"):
                break
