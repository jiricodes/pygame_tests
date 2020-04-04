from random import shuffle
from random import randrange
from copy import deepcopy

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

def create_new_path(grid, n_pieces=1):
	'''Removes random piece of wall in between [1/4 width, 1/4 height] and [3/4 width, 3/4 height]'''
	w = len(grid[0])
	h = len(grid)
	change = 0
	while change < n_pieces:
		x = randrange(int(w / 4), int(w / 4 * 3))
		y = randrange(int(h / 4), int(h / 4 * 3))
		if grid[y][x] == 1 and ((grid[y + 1][x] == 0 and grid[y - 1][x] == 0) or (grid[y][x - 1] == 0 and grid[y][x + 1] == 0)):
			grid[y][x] = 0
			print(f"Removed wall at [{x},{y}]")
			change += 1

def create_new_path_bfs(grid, start, end, n_pieces_to_remove=1):
	def get_frequency(grid, n):
		w = len(grid[0])
		h = len(grid)
		d = (w**2 + h**2) ** 0.5
		return int(d / n)

	def get_neighbors(grid, grid_width, grid_height, pos):
		x = pos[0]
		y = pos[1]
		ngbs = list()
		if x > 0 and abs(grid[y][x - 1]) != 1: #add left
			ngbs.append([x - 1, y])
		if x < grid_width - 1 and abs(grid[y][x + 1]) != 1: #add right
			ngbs.append([x + 1, y])
		if y > 0 and abs(grid[y - 1][x]) != 1: #add down
			ngbs.append([x, y - 1])
		if y < grid_height - 1 and abs(grid[y + 1][x]) != 1: #add up
			ngbs.append([x, y + 1])
		return ngbs

	def new_path(grid, w, h, position):
		x = position[0]
		y = position[1]
		if y > h / 2 and (grid[y - 2][x] == 0 or grid[y - 2][x] == -1):
			grid[y - 1][x] = 0
			print(f"Removed wall at [{x}, {y - 1}]")
			return [x, y - 1]
		elif y < h / 2 and (grid[y + 2][x] == 0 or grid[y + 2][x] == -1):
			grid[y + 1][x] = 0
			print(f"Removed wall at [{x}, {y + 1}]")
			return [x, y + 1]
		elif x > w / 2 and (grid[y][x - 2] == 0 or grid[y][x - 2] == -1):
			grid[y][x - 1] = 0
			print(f"Removed wall at [{x - 1}, {y}]")
			return [x - 1, y]
		elif x < w / 2 and (grid[y][x + 2] == 0 or grid[y][x + 2] == -1):
			grid[y][x + 1] = 0
			print(f"Removed wall at [{x + 1}, {y}]")
			return [x + 1, y]
		else:
			return None

	tmp = deepcopy(grid)
	w = len(tmp[0])
	h = len(tmp)
	queue = list()
	queue.append([start])
	cnt = 0
	if n_pieces_to_remove:
		f = get_frequency(grid, n_pieces_to_remove)
		print(f)
	while len(queue):
		path = queue.pop(0)
		current = path[-1]
		if current == end:
			grid[start[1]][start[0]] = 2
			return True, path
		ngb = get_neighbors(tmp, w, h, current)
		if len(ngb) == 0 and n_pieces_to_remove > 0:
			cnt += 1
			if cnt % f == 0:
				n_ngb = new_path(grid, w, h, current)
				if n_ngb:
					n_pieces_to_remove -= 1
					ngb.append(n_ngb)
				elif cnt > 0:
					cnt -= 1
		for n in ngb:
			new = list(path)
			new.append(n)
			queue.append(new)
		tmp[current[1]][current[0]] = -1
	return False, None

def find_start_xy(grid, w, h):
	i = 1
	while i < h:
		k = 1
		while k < w:
			if grid[i][k] == 2:
				return [k, i]
			k += 1
		i += 1
	return None

def find_end_xy(grid, w, h):
	i = h - 1
	while i > -1:
		k = w - 1
		while k > -1:
			if grid[i][k] == 3:
				return [k, i]
			k -= 1
		i -= 1
	return None

def print_grid(grid):
	for row in grid:
		for n in row:
			print(f"{n:2}", end=" ")
		print()

def reset_visited(grid, w, h):
	i = 0
	while i < h:
		k = 0
		while k < h:
			if grid[i][k] == -1:
				grid[i][k] = 0
			k += 1
		i += 1

def create_maze_depthfirst_multipath(width, height, n_pieces_to_remove):
	maze = create_maze_depthfirst(width, height)
	create_new_path_bfs(maze, find_start_xy(maze, width, height), find_end_xy(maze, width, height),n_pieces_to_remove)
	return maze

if __name__ == "__main__":
	h = 11
	w = 11
	g = create_maze_depthfirst_multipath(w,h, 3)
	print_grid(g)