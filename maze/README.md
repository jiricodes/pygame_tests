# Maze Generator
Kinda wacky maze generator using Depth First method to generate a maze and adjusted BFS to attempt extra path creation.

As of 04/04/2020 the generator cannot make maze bigger than 99x99 due to Python's recursion max depth limit (planning on workaround by splitting the generation into sector smaller than that)

## Path Finding

### BFS
Finds the shorthest path using BFS.

## Controls
Mouse click, prints to terminal current location of the mouse pointer based on the grid coordinates rather than pixels.

Keys "1" and "2" can be used to show/hide BFS path