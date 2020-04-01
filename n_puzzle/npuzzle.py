import pygame as pg
import sys
from random import shuffle

class PuzzleBoard():
	def __init__(self, n, t_size):
		self.out_margin = 0
		self.tile_size = t_size
		self.border_size = int(self.tile_size / 10)
		self.n = n
		self.size = self.n * self.tile_size + (self.n + 1) * self. border_size
		self.bg_draw_position = [self.out_margin, self.out_margin, self.size, self.size]
		self.tiles = list()
		for i in range(self.n):
			row = [0] * self.n
			self.tiles.append(row)
		self.shuffle_tiles()
		print(self.tiles)
		self.bg_color = (255, 255, 255)
		self.tile_color = (185, 185, 185)
		if self.n ** 2 > 999:
			fontsize = int(self.tile_size / 3)
		else:
			fontsize = int(self.tile_size / 2)
		self.tile_font = pg.font.Font('resources/font1.ttf', fontsize)
		self.tile_text_color = (0, 0, 0)
	
	def shuffle_tiles(self):
		pool = list(range(self.n * self.n))
		shuffle(pool)
		i = 0
		while i < self.n:
			k = 0
			while k < self.n:
				self.tiles[i][k] = pool.pop(0)
				k += 1
			i += 1

	def plot(self, window):
		pg.draw.rect(window, self.bg_color, self.bg_draw_position)
		x = self.out_margin + self.border_size
		y = self.out_margin + self.border_size
		for row in self.tiles:
			for tile in row:
				if tile:
					if self.tiles[int((tile - 1) / self.n)][int((tile - 1) % self.n)] == tile:
						color = (154, 209, 158)
					else:
						color = self.tile_color
					pg.draw.rect(window, color, [x, y, self.tile_size, self.tile_size])
					text = self.tile_font.render(f"{tile}", True, self.tile_text_color)
					text_anchor = text.get_rect()
					text_anchor.center = (x + int(self.tile_size/2), y + int(self.tile_size/2))
					window.blit(text, text_anchor)
				x += self.tile_size + self.border_size
			x = self.out_margin + self.border_size
			y += self.tile_size + self.border_size

	def find_number(self, nb):
		i = 0
		while i < self.n:
			k = 0
			while k < self.n:
				if self.tiles[i][k] == nb:
					return i, k
				k += 1
			i += 1
		print(f"Puzzle error, couldn't find {nb}!")
		exit()
	
	def move_left(self):
		i, k = self.find_number(0)
		if k < self.n - 1:
			self.tiles[i][k] = self.tiles[i][k + 1]
			self.tiles[i][k + 1] = 0
	
	def move_right(self):
		i, k = self.find_number(0)
		if k > 0:
			self.tiles[i][k] = self.tiles[i][k - 1]
			self.tiles[i][k - 1] = 0
	
	def move_up(self):
		i, k = self.find_number(0)
		if i < self.n - 1:
			self.tiles[i][k] = self.tiles[i + 1][k]
			self.tiles[i + 1][k] = 0
	
	def move_down(self):
		i, k = self.find_number(0)
		if i > 0:
			self.tiles[i][k] = self.tiles[i - 1][k]
			self.tiles[i - 1][k] = 0
		

if __name__ == "__main__":
	if len(sys.argv) == 2:
		n = int(sys.argv[1])
	else:
		n = 3
	if n < 10:
		t_size = 100
	else:
		t_size = int(1000 / (n + int((n + 1) / 10)))
	pg.init()
	win_width = n * t_size + (n + 1) * int(t_size / 10)
	win_height = n * t_size + (n + 1) * int(t_size / 10)
	root = pg.display.set_mode((win_width, win_height))
	pg.display.set_caption("N-Puzzle by jiricodes")
	gameon = True
	puzzle = PuzzleBoard(n, t_size)
	while gameon:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				gameon = False
			if event.type == pg.KEYUP:
				if event.key == pg.K_LEFT:
					puzzle.move_left()
				if event.key == pg.K_RIGHT:
					puzzle.move_right()
				if event.key == pg.K_UP:
					puzzle.move_up()
				if event.key == pg.K_DOWN:
					puzzle.move_down()
		root.fill((0, 0, 0))
		puzzle.plot(root) 
		pg.display.update()