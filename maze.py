"""Maze generator and solver.

Generates a perfect maze (exactly one path between any two cells) using
randomized depth-first search, then finds the shortest path from the top-left
to the bottom-right corner with a breadth-first search.

Usage:
    python maze.py                # 21x21 maze, random seed
    python maze.py --width 31 --height 21 --seed 42
"""

import argparse
import random
from collections import deque

# Cell flags
WALL = "#"
PATH = " "
SOLUTION = "."

# Movement: (row_delta, col_delta)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def generate(width, height, rng):
    """Carve a perfect maze using iterative randomized DFS.

    The grid uses odd dimensions so that cells sit on odd indices and walls
    on even ones. We carve passages two cells at a time.
    """
    grid = [[WALL for _ in range(width)] for _ in range(height)]
    start = (1, 1)
    grid[start[0]][start[1]] = PATH
    stack = [start]

    while stack:
        r, c = stack[-1]
        neighbours = []
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr * 2, c + dc * 2
            if 1 <= nr < height - 1 and 1 <= nc < width - 1 and grid[nr][nc] == WALL:
                neighbours.append((nr, nc, dr, dc))

        if not neighbours:
            stack.pop()
            continue

        nr, nc, dr, dc = rng.choice(neighbours)
        grid[r + dr][c + dc] = PATH  # knock down the wall between cells
        grid[nr][nc] = PATH
        stack.append((nr, nc))

    return grid


def solve(grid):
    """Return the shortest path from top-left to bottom-right via BFS."""
    height, width = len(grid), len(grid[0])
    start, goal = (1, 1), (height - 2, width - 2)

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        r, c = current
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if (
                0 <= nr < height
                and 0 <= nc < width
                and grid[nr][nc] != WALL
                and nxt not in came_from
            ):
                came_from[nxt] = current
                queue.append(nxt)

    if goal not in came_from:
        return []

    # Reconstruct the path by walking backwards from the goal.
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


def render(grid, path=None):
    """Return the maze as a string, marking the solution path if given."""
    path_set = set(path or [])
    lines = []
    for r, row in enumerate(grid):
        chars = []
        for c, cell in enumerate(row):
            if (r, c) in path_set and cell != WALL:
                chars.append(SOLUTION)
            else:
                chars.append(cell)
        lines.append("".join(chars))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate and solve a maze.")
    parser.add_argument("--width", type=int, default=21, help="maze width (odd)")
    parser.add_argument("--height", type=int, default=21, help="maze height (odd)")
    parser.add_argument("--seed", type=int, default=None, help="random seed")
    args = parser.parse_args()

    # Force odd dimensions so the wall/cell layout works out.
    width = args.width | 1
    height = args.height | 1
    rng = random.Random(args.seed)

    grid = generate(width, height, rng)
    path = solve(grid)

    print("Maze:\n")
    print(render(grid))
    print(f"\nSolution ({len(path)} steps):\n")
    print(render(grid, path))


if __name__ == "__main__":
    main()
