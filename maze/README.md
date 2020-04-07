# Maze Generator
Kinda wacky maze generator using Depth First method to generate a maze and adjusted BFS to attempt extra path creation.

As of 04/04/2020 the generator cannot make maze bigger than 90x90 due to Python's recursion max depth limit (planning on workaround by splitting the generation into sector smaller than that)

## Path Finding

### BFS
Finds the shortest path using BFS.

### A*
Finds the shortest path using A*.
Currently implemented heuristics:
	- Manhattan

Returns also trace which can be animated.

## Controls
### Basic
Mouse click, prints to terminal current location of the mouse pointer based on the grid coordinates rather than pixels.

Keys "1" and "2" can be used to show/hide BFS path and A* path respectively (they should be matching tho)

Space Bar to animate start/pause BFS path animation. Arrow keys Left and Right to animate it manually.

### Tracing
Key "T" to start A* trace animation.

Keys "+" and "-" on numpad to increase animation speed.

Key "R" to restart.