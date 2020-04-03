def grid_index_to_coords(grid_width, grid_height, index):
	x = index % grid_width
	y = index // grid_height
	return [x, y]

def grid_coords_to_index(grid_height, coords):
	i = grid_height * coords[1] + coords[0]
	return i

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

def bfs_path(grid, start, end):
	tmp = grid.copy()
	w = len(tmp[0])
	h = len(tmp)
	queue = list()
	queue.append([start])
	while len(queue):
		path = queue.pop(0)
		current = path[-1]
		if current == end:
			return True, path
		for n in get_neighbors(tmp, w, h, current):
			new = list(path)
			new.append(n)
			queue.append(new)
		tmp[current[1]][current[0]] = -1
	return False, tmp