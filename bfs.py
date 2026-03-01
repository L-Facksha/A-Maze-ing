from typing import List


def bfs(grid, entry: tuple[int, int], end: tuple[int, int]):
    queue = []
    visited = []
    couple: List[List[tuple]] = []
    queue.append(entry)
    visited.append(entry)
    er, ec = end
    while queue:
        y, x = queue.pop(0)
        if y == er and x == ec:
            break
        if (grid[y][x] & 1) == 0 and (y - 1, x) not in visited:
            queue.append((y - 1, x))
            visited.append((y - 1, x))
            couple.append(((y, x), (y - 1, x)))
        if (grid[y][x] & 2) == 0 and (y, x + 1) not in visited:
            queue.append((y, x + 1))
            visited.append((y, x + 1))
            couple.append(((y, x), (y, x + 1)))
        if (grid[y][x] & 4) == 0 and (y + 1, x) not in visited:
            queue.append((y + 1, x))
            visited.append((y + 1, x))
            couple.append(((y, x), (y + 1, x)))
        if (grid[y][x] & 8) == 0 and (y, x - 1) not in visited:
            queue.append((y, x - 1))
            visited.append((y, x - 1))
            couple.append(((y, x), (y, x - 1)))

    curr = end
    path = []
    while curr != entry:
        path.append(curr)
        for p, c in couple:
            if c == curr:
                curr = p
                break
    path.append(entry)
    path.reverse()
    return path
