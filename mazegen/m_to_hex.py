import sys
from typing import List


def m_to_hex(grid: List[List[int]], entry: tuple[int, int], end: tuple[int, int], width: int, height: int, path: List[tuple[int, int]], output_file: str) -> None: # noqa
    """
    Convert a maze grid into hexadecimal representation and write it to a file.

    Each cell in the grid is assumed to use bitwise wall encoding:
        1 -> wall present
        2 -> wall present
        4 -> wall present
        8 -> wall present

    The function:
    - Converts each cell’s bitwise value into a hexadecimal digit.
    - Writes the hexadecimal maze layout to "output_maze.txt".
    - Writes the entry and exit coordinates.
    - Converts the solution path into directional steps:
        E (East), W (West), N (North), S (South).

    Args:
        grid: 2D list representing the maze with bitwise wall encoding.
        entry: Tuple (row, col) representing the maze entry point.
        end: Tuple (row, col) representing the maze exit point.
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        path: List of (row, col) tuples representing the solution path.

    Returns:
        None. Output is written to "output_maze.txt".
    """
    llist: List[List[str]] = []
    hex: List[str] = ["A", "B", "C", "D", "E", "F"]
    n: int = 0
    row: int = 0
    original_stdout = sys.stdout
    with open(output_file, "w") as f:
        sys.stdout = f
        while row < height:
            col: int = 0
            r: List[str] = []
            while col < width:
                if (grid[row][col] & 1) != 0:
                    n += 1
                if (grid[row][col] & 2) != 0:
                    n += 2
                if (grid[row][col] & 4) != 0:
                    n += 4
                if (grid[row][col] & 8) != 0:
                    n += 8
                if 9 < n < 16:
                    r.append(hex[n - 10])
                else:
                    r.append(str(n))
                n = 0
                col += 1
            llist.append(r)
            row += 1
        i = 0
        while i < height:
            col = 0
            while col < width:
                print(f"{llist[i][col]}", end="")
                col += 1
            i += 1
            print()
        print()
        sc, sr = entry
        ec, er = end
        print(f"{sc},{sr}")
        print(f"{ec},{er}")
        i = 0
        d: List[str] = []
        while i < len(path) - 1:
            cc, cr = path[i]
            nc, nr = path[i + 1]
            if nr == cr and nc == cc + 1:
                d.append("E")
            elif nr == cr and nc == cc - 1:
                d.append("W")
            elif nr == cr - 1 and nc == cc:
                d.append("N")
            else:
                d.append("S")
            i += 1
        i = 0
        while i < len(d):
            print(f"{d[i]}", end="")
            i += 1
        print()
    sys.stdout = original_stdout
