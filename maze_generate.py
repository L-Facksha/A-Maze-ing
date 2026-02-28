import curses


def display(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED,   curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA,  curses.COLOR_BLACK)

    message = "Hello Maze!"
    color_index = 1          # track current color

    while True:
        stdscr.clear()

        # use color_index to draw
        stdscr.addstr(0, 0, message, curses.color_pair(color_index))
        stdscr.addstr(2, 0, "q = quit", curses.color_pair(1))
        stdscr.addstr(3, 0, "c = change color", curses.color_pair(1))
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('c'):
            # cycle through colors 1 2 3 4 1 2 3 4 ...
            color_index = (color_index % 4) + 1


curses.wrapper(display)
