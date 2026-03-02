import sys


def m_to_hex(grid, entry, end, width, height, path):
    llist = []
    r = []
    hex = ["A", "B", "C", "D", "E", "F"]
    n = 0
    row = 0
    original_stdout = sys.stdout
    with open("output_maze.txt", "w") as f:
        sys.stdout = f
        while row < height:
            r = []
            col = 0
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
                    n -= 10
                    n = hex[n]
                r.append(n)
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
        sr, sc = entry
        er, ec = end
        print(f"{sr},{sc}")
        print(f"{er},{ec}")
        i = 0
        d = []
        while i < len(path) - 1:
            cr, cc = path[i]
            nr, nc = path[i + 1]
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
