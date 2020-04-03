from random import shuffle
from random import randrange

def create_grid_checkered(width, height):
	grid = list()
	for r in range(height):
		row = list()
		for c in range(width):
			if r == 0 or c == 0 or r == height - 1 or c == width - 1:
				row.append(1)
			elif c % 2 and r % 2:
				row.append(0)
			else:
				row.append(1)
		grid.append(row)
	return grid

def create_maze_depthfirst(width, height):
	maze = create_grid_checkered(width, height)
	
	w = (width - 1) // 2
	h = (height - 1) // 2
	vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

	def walk(x, y):
		vis[y][x] = 1

		next_step = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
		shuffle(next_step)
		for (new_x, new_y) in next_step:
			if vis[new_y][new_x]:
				continue
			if new_x == x:
				maze[max(y, new_y) * 2][x * 2 + 1] = 0
			if new_y == y:
				maze[y * 2 + 1][max(x, new_x) * 2] = 0
			walk(new_x, new_y)
	walk(randrange(w), randrange(h))
	notdone = True
	i = 1
	while i < height and notdone:
		k = 1
		while k < width and notdone:
			if maze[i][k] == 0:
				maze[i][k] = 2
				notdone = False
			k += 1
		i += 1
	notdone = True
	i = height - 1
	while i > -1 and notdone:
		k = width - 1
		while k > -1 and notdone:
			if maze[i][k] == 0:
				maze[i][k] = 3
				notdone = False
			k -= 1
		i -= 1
	return maze

def print_grid(grid):
	for row in grid:
		for n in row:
			print(n, end=" ")
		print()

if __name__ == "__main__":
	g = create_maze_depthfirst(11,11)
	print_grid(g)