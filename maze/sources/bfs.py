from copy import deepcopy

def get_neighbors(grid, grid_width, grid_height, pos):
	x = pos[0]
	y = pos[1]
	ngbs = list()
	if x > 0 and abs(grid[y][x - 1]) != 1: #add left
		ngbs.append([x - 1, y])
		grid[y][x - 1] = -1
	if x < grid_width - 1 and abs(grid[y][x + 1]) != 1: #add right
		ngbs.append([x + 1, y])
		grid[y][x + 1] = -1
	if y > 0 and abs(grid[y - 1][x]) != 1: #add down
		ngbs.append([x, y - 1])
		grid[y - 1][x] = -1
	if y < grid_height - 1 and abs(grid[y + 1][x]) != 1: #add up
		ngbs.append([x, y + 1])
		grid[y + 1][x] = - 1
	return ngbs

def bfs_path(grid, start, end):
	if not grid or not start or not end:
		return False, None, None
	cnt = 0
	tmp = deepcopy(grid)
	w = len(tmp[0])
	h = len(tmp)
	queue = list()
	queue.append([start])
	trace = list()
	while len(queue):
		path = queue.pop(0)
		current = path[-1]
		if current != start:
			trace.append(path)
		if current == end:
			print(f"BFS Explored Vertices: {cnt}")
			return True, path, trace
		for n in get_neighbors(tmp, w, h, current):
			new = list(path)
			new.append(n)
			queue.append(new)
		# tmp[current[1]][current[0]] = -1
		# for line in tmp:
		# 	print(line)
		# print()
		cnt += 1
		# if cnt > 10:
		# 	exit()
	print(f"BFS Explored Vertices: {cnt}")
	return False, None, None