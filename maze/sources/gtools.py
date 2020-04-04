def grid_index_to_coords(grid_width, grid_height, index):
	x = index % grid_width
	y = index // grid_height
	return [x, y]

def grid_coords_to_index(grid_height, coords):
	i = grid_height * coords[1] + coords[0]
	return i