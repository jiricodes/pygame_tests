def find_number_coords(matrix, number):
	'''Returns position of given number in two dimensional square array. Assumes correctness of the input'''
	i = 0
	l = len(matrix)
	while i < l:
		k = 0
		while k < l:
			if matrix[i][k] == number:
				return i, k
			k += 1
		i += 1
	return None, None

def print_matrix(mastrix):
	width = len(str(len(mastrix) ** 2)) + 1
	for row in mastrix:
		for nb in row:
			print(f"{nb:{width}}", end=" ")
		print()

def manhattan_distance(matrix, nb):
	pos_y, pos_x = find_number_coords(matrix, nb)
	dest_x = int((nb - 1) % len(matrix))
	dest_y = int((nb - 1) / len(matrix))
	return abs(dest_x - pos_x) + abs(dest_y - pos_y)

def zero_to_position(matrix, nb, side):
	zero_y, zero_x = find_number_coords(matrix, 0)
	avoid_y, avoid_x = find_number_coords(matrix, nb)
	

if __name__ == "__main__":
	my_matrix = [[16, 15, 22, 24, 19], [5, 18, 3, 13, 4], [11, 14, 1, 21, 8], [2, 0, 17, 9, 10], [23, 20, 6, 12, 7]]
	print(manhattan_distance(my_matrix,1))
	print_matrix(my_matrix)