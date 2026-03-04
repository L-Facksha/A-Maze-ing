# A-Maze-ing

*This project has been created as part of the 42 curriculum by azebahad, otazelma.*

---

## Description

A-Maze-ing is a Python maze generator and solver. It generates a maze from a
config file, displays it interactively in the terminal, and finds the
shortest path from entry to exit. The process involves parsing the arguments
from the config file and making the grid, then open the path using DFS (Depth-First Search algorithm)
and inserting a 42 pattern if the size is right, then with the help of BFS
(Breadth-First Search) finding the shortest path, and finally print everything to an output file. 

---

## Instructions

### Requirements
- Python 3.10 or later
- flake8
- mypy

### Installation

```bash
git clone <the-repo-url>
cd A-Maze-ing
make install
```

### Run

```bash
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

### Clean

```bash
make clean
```

---

## Config File

```
WIDTH=20              # maze width in cells
HEIGHT=15             # maze height in cells
ENTRY=0,0            # entry position (col, row)
EXIT=19,14           # exit position (col, row)
OUTPUT_FILE=maze.txt  # output file path
PERFECT=True          # True = one path, False = multiple paths
SEED=42               # optional: seed for reproducibility
```

### Rules
- `WIDTH` and `HEIGHT` must be positive integers
- `ENTRY` and `EXIT` must be inside the grid
- `ENTRY` and `EXIT` must not overlap the 42 pattern
- `OUTPUT_FILE` must end with .txt
- `SEED` is optional — if omitted maze is random each run
- `PERFECT` must be True or False
```
The config file must contain one KEY = VALUE per line.
Keys are case-sensitive.
The order of fields does not matter.
```

---

## Maze Generation Algorithm

### Recursive Backtracker (DFS)

1. Start with all walls closed
2. Pick entry cell, mark visited
3. Pick random unvisited neighbor → carve wall → move to it
4. No neighbors → backtrack
5. Repeat until all cells visited

### Why DFS

- Simple to implement
- Produces long winding corridors
- Visits every cell exactly once
- Easy to reproduce with a seed
- Easy to make imperfect by removing extra walls

---

## Maze Solving Algorithm

### Breadth-First Search

1. Take the generated grid.
2. Start from the entry, mark it as visited, and add it to a queue.
3. For each neighbor:
   - Mark as visited
   - Store parent reference
   - Add to queue
4. Stop when the exit is reached.
5. Reconstruct the path from exit to entry using parent references.
6. Reverse the path to obtain the final solution.

## Reusable Package — mazegen

It has everything anyone needs in order to generate and use the maze anywhere you want

### Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Grid Format

Each cell is an integer bitmask:
```
N=1  E=2  S=4  W=8
15 = 1111 = all walls closed
14 = 1110 = North wall open and so on for other directions
```

### Build From Source

```bash
cd mazegen
python3 -m build
```
### Usage Example

here is a snipet explaining how does everything work
```
from mazegen import MazeGenerator
from mazegen import bfs
from m_to_hex import m_to_hex

# Create a 15x10 maze with a fixed seed
gen = MazeGenerator(width=15, height=10, seed=42)

# Generate the maze (perfect by default)
grid = gen.generate()

# Solve from entry (0,0) to exit (14,9)
path = bfs(grid, entry=(0,0), exit=(14,9), width=15, height=10)

# Display the maze on the terminal
curses.wrapper(print_maze, grid, width=15, height=10, config_file, path: BFS SOLVE, 42_pattern: THE STATIC 42 FOR DISPLAY)

# Get the OUTPUT_FILE
m_to_hex(grid, entry=(0,0), exit=(14,9), width=15, height=10, path: BFS SOLVE, output_file: HEX OUTPUT)

```

---

## Team and Project Management

### Roles

| Member     | Role                                                           |
|------------|----------------------------------------------------------------|
| azebahad   | DFS generation, curses display, config parser, mazegen package |
| otazelma   | BFS pathfinding, Makefile, Hexadecimal OUTPUT_FILE             |

### Planning

**Anticipated:**
- day 2: Config parser + maze generation
- day 3: Curses display + BFS
- day 5: Package + lint + documentation

**Reality:**
- Config and generation went as planned
- Curses display took longer due to coordinate bugs 
- BFS was harder than expected and took way too long to debug and get running
- Package and documentation done at the end but took too long
### What Worked Well
- DFS was clean and easy to implement
- Separating display from generation made code cleaner
- The hexadecimal file was easy to make

### What Could Be Improved
- Add more generation algorithms
- Add animations for both generation and solving
- Better error messages in curses display

### Tools Used
- VSCode — code editor
- Git — version control
- Claude AI — used for debugging, explaining curses and BFS concepts

---

## Resources

- [Maze Generation — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Mazes for Programmers](https://www.kufunda.net/publicdocs/Mazes%20for%20Programmers%20Code%20Your%20Own%20Twisty%20Little%20Passages%20(Jamis%20Buck).pdf)
- [Recursive Backtracker — Jamis Buck](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Python curses](https://docs.python.org/3/library/curses.html)
- [BFS — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [BFS](https://www.youtube.com/watch?v=xlVX7dXLS64)
- [BFS](https://www.youtube.com/watch?v=7Cox-J7onXw)
- [Python packaging](https://packaging.python.org/en/latest/)
- [mypy](https://mypy.readthedocs.io/)
- [flake8](https://flake8.pycqa.org/)

### AI Usage

Claude AI (Anthropic) was used for:
- Explaining curses display concepts
- Helping and explaining part of the DFS and BFS
- Explaining about how does curses display in the terminal
- Debugging an issue in the BFS algorithm
```
All code implementation was written by the team. No AI-generated code was used.
``` 