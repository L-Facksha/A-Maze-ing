from typing import List


def bfs(grid: List[List[int]], entry: tuple[int, int], end: tuple[int, int], width: int, height: int) -> List[tuple[int, int]]: # noqa
    """
    Perform Breadth-First Search (BFS) to find the shortest path
    from entry to end in a maze grid.

    The grid uses bitwise values to represent walls:
        1 = North wall
        2 = East wall
        4 = South wall
        8 = West wall

    Args:
        grid: 2D list representing the maze structure.
        entry: Starting cell coordinates (row, column).
        end: Target cell coordinates (row, column).
        width: Width of the maze.
        height: Height of the maze.

    Returns:
        A list of (row, column) tuples representing the shortest
        path from entry to end. Returns an empty list if no path exists.
    """
    queue: List[tuple[int, int]] = []
    visited: List[tuple[int, int]] = []
    couple: List[tuple[tuple[int, int], tuple[int, int]]] = []
    queue.append(entry)
    visited.append(entry)
    ec, er = end
    while queue:
        x, y = queue.pop(0)
        if y == er and x == ec:
            break
        if 0 <= x < width and 0 <= y < height and (grid[y][x] & 1) == 0 and (x, y - 1) not in visited: # noqa
            queue.append((x, y - 1))
            visited.append((x, y - 1))
            couple.append(((x, y), (x, y - 1)))
        if 0 <= x < width and 0 <= y < height and (grid[y][x] & 2) == 0 and (x + 1, y) not in visited: # noqa
            queue.append((x + 1, y))
            visited.append((x + 1, y))
            couple.append(((x, y), (x + 1, y)))
        if 0 <= x < width and 0 <= y < height and (grid[y][x] & 4) == 0 and (x, y + 1) not in visited: # noqa
            queue.append((x, y + 1))
            visited.append((x, y + 1))
            couple.append(((x, y), (x, y + 1)))
        if 0 <= x < width and 0 <= y < height and (grid[y][x] & 8) == 0 and (x - 1, y) not in visited: # noqa
            queue.append((x - 1, y))
            visited.append((x - 1, y))
            couple.append(((x, y), (x - 1, y)))

    curr = end
    path: List[tuple[int, int]] = []
    if curr not in visited:
        return []
    while curr != entry:
        path.append(curr)
        for p, c in couple:
            if c == curr:
                curr = p
                break
    path.append(entry)
    path.reverse()
    return path
