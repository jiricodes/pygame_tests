import arcade as ar
import sys
import os
from random import shuffle
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

class PuzzleBoard(ar.Window):
	def __init__(self, n, t_size, win_width, win_height):
		super().__init__(win_width, win_height, "N-Puzzle by jiricodes")
		# file_path = os.path.dirname(os.path.abspath(__file__))
		# os.chdir(file_path)
		self.out_margin = 0
		self.tile_size = t_size
		self.tile_ratio = t_size / 200
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
			self.tile_fontsize = int(self.tile_size / 2)
		else:
			self.tile_fontsize = int(self.tile_size / 5 * 4)
		self.tile_font = 'resources/font1.ttf'
		self.tile_text_color = (0, 0, 0)
		self.tiles_sprites = None
		self.tiles_list = list()
		self.tiles_textures = None
		ar.set_background_color(ar.color.BLACK)
		self.tile_speed = 5
		self.tile_moving = None
	
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

	def setup(self):
		self.tiles_sprites = ar.SpriteList()
		self.tiles_textures = list()
		i = 1
		while i < self.n ** 2:
			i_file = Image.open('resources/puzzle_tile.png')
			img = ImageDraw.Draw(i_file)
			font = ImageFont.truetype(self.tile_font, self.tile_fontsize)
			text = f"{i}"
			text_w, text_h = img.textsize(text, font)
			img.text((int(100 - text_w / 2), int(100 - text_h / 5 * 3)), text, fill=self.tile_text_color, font=font)
			texture = ar.Texture(text, i_file)
			self.tiles_textures.append(texture)
			i += 1
		x = self.out_margin + self.border_size + int(200 * self.tile_ratio / 2)
		y = self.size - self.border_size - int(200 * self.tile_ratio / 2)
		i = 0
		while i < self.n:
			k = 0
			row = list()
			while k < self.n:
				if self.tiles[i][k]:
					new = ar.Sprite()
					new.texture = self.tiles_textures[self.tiles[i][k] - 1]
					new.scale = self.tile_ratio
					new.center_y = y
					new.center_x = x
					self.tiles_sprites.append(new)
					row.append(new)
				else:
					row.append(None)
				x += int(200 * self.tile_ratio) + self.border_size
				k += 1
			self.tiles_list.append(row)
			x = self.out_margin + self.border_size + int(200 * self.tile_ratio / 2)
			y -= int(200 * self.tile_ratio) + self.border_size
			i += 1
		self.time_elapsed = 0
		print(self.tiles_list)

	def on_draw(self):
		ar.start_render()
		self.tiles_sprites.draw()
	
	def on_update(self, delta_time):
		if self.tile_moving:
			print("Tile's moving!")
			i = 0
			while i < self.n:
				k = 0
				while k < self.n:
					if self.tiles_list[i][k] and not (self.tile_moving['row'] == i and self.tile_moving['column'] == k):
						delta_x = abs(self.tiles_list[i][k].center_x - self.tile_moving['sprite'].center_x)
						delta_y = abs(self.tiles_list[i][k].center_y - self.tile_moving['sprite'].center_y)
						spacer = 200 * self.tile_ratio + self.border_size
						print(f"{delta_x} | {delta_y} | {spacer}")
						if delta_x < spacer and delta_y < spacer:
							self.tile_moving['sprite'].change_x = 0
							self.tile_moving['sprite'].change_y = 0
							self.tile_moving['sprite']
							self.tile_moving = None
							break
					k += 1
				if self.tile_moving == None:
					break
				i += 1
		# else:
		# 	print("Tile's not moving!")
		self.tiles_sprites.update()
	
	def on_key_release(self, symbol, modifiers):
		if symbol == ar.key.RIGHT:
			self.move_right()
		if symbol == ar.key.LEFT:
			self.move_left()
		if symbol == ar.key.UP:
			self.move_up()
		if symbol == ar.key.DOWN:
			self.move_down()

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
		if k < self.n - 1 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i][k + 1]
			self.tiles[i][k + 1] = 0
			self.tiles_list[i][k] = self.tiles_list[i][k + 1]
			self.tiles_list[i][k + 1] = None
			self.tiles_list[i][k].change_x = -1 * self.tile_speed
			self.tile_moving = { 'row': i, 'column': k, 'sprite': self.tiles_list[i][k]}

	def move_right(self):
		i, k = self.find_number(0)
		if k > 0 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i][k - 1]
			self.tiles[i][k - 1] = 0
			self.tiles_list[i][k] = self.tiles_list[i][k - 1]
			self.tiles_list[i][k - 1] = None
			self.tiles_list[i][k].change_x = self.tile_speed
			self.tile_moving = { 'row': i, 'column': k, 'sprite': self.tiles_list[i][k]}

	def move_up(self):
		i, k = self.find_number(0)
		if i < self.n - 1 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i + 1][k]
			self.tiles[i + 1][k] = 0
			self.tiles_list[i][k] = self.tiles_list[i + 1][k]
			self.tiles_list[i + 1][k] = 0
			self.tiles_list[i][k].change_y = self.tile_speed
			self.tile_moving = { 'row': i, 'column': k, 'sprite': self.tiles_list[i][k]}
	
	def move_down(self):
		i, k = self.find_number(0)
		if i > 0 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i - 1][k]
			self.tiles[i - 1][k] = 0
			self.tiles_list[i][k] = self.tiles_list[i - 1][k]
			self.tiles_list[i - 1][k] = 0
			self.tiles_list[i][k].change_y = -1 * self.tile_speed
			self.tile_moving = { 'row': i, 'column': k, 'sprite': self.tiles_list[i][k]}



def run_game(n, t_size, win_width, win_height):
	'''Main'''
	window = PuzzleBoard(n, t_size, win_width, win_height)
	window.setup()
	ar.run()

if __name__ == "__main__":
	
	if len(sys.argv) == 2:
		n = int(sys.argv[1])
	else:
		n = 5
	if n < 10:
		t_size = 100
	else:
		t_size = int(1000 / (n + int((n + 1) / 10)))
	win_width = n * t_size + (n + 1) * int(t_size / 10)
	win_height = n * t_size + (n + 1) * int(t_size / 10)
	run_game(n, t_size, win_width, win_height)