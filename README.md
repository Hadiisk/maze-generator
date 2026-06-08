# Maze Generator & Solver

Generates a **perfect maze** (exactly one path between any two cells) and then
finds the shortest route through it. Pure Python, no dependencies.

## How it works

**Generation** uses randomized depth-first search. Starting from one cell, it
carves passages to random unvisited neighbours two cells away, backtracking
whenever it hits a dead end. Because it never connects two already-visited
regions, the result is a maze with no loops.

**Solving** uses breadth-first search, which is guaranteed to find the shortest
path in an unweighted grid. The path is reconstructed by walking backwards
through the `came_from` map from goal to start.

## Usage

```bash
python maze.py                              # 21x21 maze
python maze.py --width 31 --height 21       # custom size
python maze.py --seed 42                    # reproducible maze
```

Dimensions are forced to odd numbers so walls and cells line up correctly.

## Example output

```
Maze:

#########
#       #
# ### # #
#   # # #
### # ###
#   #   #
#########

Solution (.) marks the path from top-left to bottom-right.
```

## Files

| File | Purpose |
| --- | --- |
| `maze.py` | Generator, BFS solver, and CLI |
