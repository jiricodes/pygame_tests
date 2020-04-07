from copy import deepcopy
from collections import defaultdict

def i_to_xy(grid_width, grid_height, index):
	x = index % grid_width
	y = index // grid_height
	return [x, y]

def xy_to_i(grid_height, coords):
	i = grid_height * coords[1] + coords[0]
	return i

def manhattan_heuristic(grid, end):
	manhattan = deepcopy(grid)
	w = len(manhattan[0])
	h = len(manhattan)
	x = end[0]
	y = end[1]
	manhattan[y][x] = 0
	i = 0
	while i < h:
		k = 0
		while k < w:
			manhattan[i][k] = abs(x - k) + abs(y - i)
			k += 1
		i += 1
	return manhattan

def euclidean_heuristic(grid, end):
	euclid = deepcopy(grid)
	w = len(euclid[0])
	h = len(euclid)
	x = end[0]
	y = end[1]
	euclid[y][x] = 0
	i = 0
	while i < h:
		k = 0
		while k < w:
			euclid[i][k] = ((x - k) ** 2 + (y - i) ** 2) ** 0.5
			k += 1
		i += 1
	return euclid

def get_heuristic_grid(grid, end, name):
	heuristics = {
		'manhattan': manhattan_heuristic(grid, end),
		'euclid' : euclidean_heuristic(grid, end)
	}
	if name in heuristics.keys():
		return heuristics[name]
	else:
		return None

def astar_path(grid, start, end, h_name):
	def get_neighbors_valid(grid, w, h, index, closed):
		position = i_to_xy(w, h, index)
		x = position[0]
		y = position[1]
		neighbors = list()
		if x > 0 and grid[y][x - 1] != 1:
			left =  xy_to_i(h, [x - 1, y])
			if not left in closed.keys():
				neighbors.append(left)
		if x < w - 1 and grid[y][x + 1] != 1:
			right =  xy_to_i(h, [x + 1, y])
			if not right in closed.keys():
				neighbors.append(right)
		if y > 0 and grid[y - 1][x] != 1:
			up =  xy_to_i(h, [x, y - 1])
			if not up in closed.keys():
				neighbors.append(up)
		if y < h - 1 and grid[y + 1][x] != 1:
			down =  xy_to_i(h, [x, y + 1])
			if not down in closed.keys():
				neighbors.append(down)
		return neighbors

	def get_h(heuristic, width, height, index):
		loc = i_to_xy(width, height, index)
		return heuristic[loc[1]][loc[0]]

	def create_returnvalues(w, h, result, start, end):
		i_path = list()
		current = end
		while current != start:
			i_path.insert(0, current)
			current = result[i_path[0]][3]
		i_path.insert(0, current)
		path = list()
		for i in i_path:
			new = i_to_xy(w, h, i)
			path.append(new)
		return path

	w = len(grid[0])
	h = len(grid)
	heuristic = get_heuristic_grid(grid, end, h_name)
	if not heuristic:
		return False, None, None
	cost = 1
	end_index = xy_to_i(h, end)
	start_index = xy_to_i(h, start)
	opened = defaultdict(int)
	# Values are lists as [total_cost, g_cost, h_cost, parent]
	opened[start_index] = [heuristic[start[1]][start[0]], 0, heuristic[start[1]][start[0]], -1]
	closed = defaultdict(int)
	cnt = 0
	trace = list()
	while len(opened):
		current = sorted(opened, key=opened.get)[0]
		# for item in sorted(opened, key=opened.get):
		# 	print(f"{item:5}:{opened[item][0]:8.3f} |{opened[item][1]:5} |{opened[item][2]:8.3f} |{opened[item][3]:5} |")
		# print("-"*50)
		# if current > w * 20:
		# 	exit()
		current_data = opened.pop(current)
		closed[current] = current_data
		if current != start_index:
			trace.append(create_returnvalues(w,h,closed, start_index, current))
		cnt += 1
		if current == end_index:
			print("Path found")
			print(f"A* visited vertices: {cnt}")
			return True, create_returnvalues(w, h, closed, start_index, end_index), trace
		for ngb in get_neighbors_valid(grid, w, h, current, closed):
			ngb_gcost = current_data[1] + cost
			ngb_hcost = get_h(heuristic, w, h, ngb)
			ngb_cost = ngb_gcost + ngb_hcost
			if ngb not in opened.keys():
				opened[ngb] = [ngb_cost, ngb_gcost, ngb_hcost, current]
			elif opened[ngb][0] > ngb_cost:
				opened[ngb][0] = ngb_cost
				opened[ngb][1] = ngb_gcost
				opened[ngb][2] = ngb_hcost
				opened[ngb][3] = current
	print("Path not found")
	print(f"A* visited vertices: {cnt}")
	return False, None, None

if __name__ == "__main__":
	w = 5
	h = 5
	g = list()
	for i in range(h):
		row = list()
		for k in range(w):
			row.append(0)
		g.append(row)
	print(g)
	h = get_heuristic_grid(g, [3,3], 'euclid')
	for row in h:
		print(row)