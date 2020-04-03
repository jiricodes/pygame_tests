import arcade as ar
import sys
import os
from random import shuffle
from random import randint
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
		self.create_tiles_values()
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
		self.tile_speed_orig = 15
		self.tile_speed = self.tile_speed_orig
		self.tile_moving = None
		self.tile_travel_distance = self.tile_size + self.border_size
		self.shuffle_iterations = 0
		self.last_move = None
		self.gameon = True
		self.win_img = None
		self.restart_img = None
	
	def create_tiles_values(self):
		pool = list(range(self.n * self.n))
		zero = pool.pop(0)
		pool.append(zero)
		i = 0
		while i < self.n:
			k = 0
			while k < self.n:
				self.tiles[i][k] = pool.pop(0)
				k += 1
			i += 1

	def shuffle_tiles(self):
		self.gameon = True
		self.shuffle_iterations = self.n ** 2 * 25
		self.tile_speed = self.shuffle_iterations ** 3
		self.random_move()

	def random_move(self):
		def is_oposite(a, b):
			if (a, b) == (0, 1) or (a, b) == (1, 0) or (a, b) == (2, 3) or (a, b) == (3, 2):
				return True
			else:
				return False
		generate = True
		while generate:
			m = randint(0, 3)
			if not is_oposite(m, self.last_move):
				generate = False
		if m == 0:
			if not self.move_right():
				self.random_move()
				return
		elif m == 1:
			if not self.move_left():
				self.random_move()
				return
		elif m == 2:
			if not self.move_up():
				self.random_move()
				return
		else:
			if not self.move_down():
				self.random_move()
				return
		self.last_move = m

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
		self.win_img = ar.Sprite('resources/victory.png', self.size/1000)
		self.win_img.center_x = self.size / 2
		self.win_img.center_y = self.size / 4 * 3
		self.restart_img = ar. Sprite('resources/restart.png', self.size/1000)
		self.restart_img.center_x = self.size / 2
		self.restart_img.center_y = self.size / 4
		self.time_elapsed = 0
		self.shuffle_tiles()

	def draw_end_game(self):
		self.win_img.draw()
		self.restart_img.draw()

	def on_draw(self):
		ar.start_render()
		if self.gameon:
			self.tiles_sprites.draw()
		else:
			self.draw_end_game()
	
	def on_update(self, delta_time):
		if self.tile_moving:
			delta_x = abs(self.tile_moving['sprite'].center_x - self.tile_moving['dest_x'])
			delta_y = abs(self.tile_moving['sprite'].center_y - self.tile_moving['dest_y'])
			error_margin = self.border_size / 2 + self.tile_speed
			if delta_x < error_margin and delta_y < error_margin:
				self.tile_moving['sprite'].change_x = 0
				self.tile_moving['sprite'].change_y = 0
				self.tile_moving['sprite'].center_x = self.tile_moving['dest_x']
				self.tile_moving['sprite'].center_y = self.tile_moving['dest_y']
				self.tile_moving = None
		else:
			if self.shuffle_iterations:
				self.random_move()
				self.shuffle_iterations -= 1
			else:
				self.tile_speed = self.tile_speed_orig
				if self.check_end():
					self.gameon = False
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
		if symbol == ar.key.R:
			self.shuffle_tiles()
		if symbol == ar.key.NUM_ADD or symbol == ar.key.E:
			self.tile_speed_orig += 5
			print(f"PLUS | Original {self.tile_speed_orig} | Current {self.tile_speed}")
		if (symbol == ar.key.NUM_SUBTRACT or symbol == ar.key.Q) and self.tile_speed > 5:
			self.tile_speed_orig -= 5
			print(f"MINUS | Original {self.tile_speed_orig} | Current {self.tile_speed}")
		if symbol == ar.key.EQUAL or symbol == ar.key.W:
			self.tile_speed_orig = 15
			print(f"EQUAL | Original {self.tile_speed_orig} | Current {self.tile_speed}")

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
			self.tile_moving = { 'dest_y': self.tiles_list[i][k].center_y, 'dest_x': self.tiles_list[i][k].center_x  - self.tile_travel_distance, 'sprite': self.tiles_list[i][k]}
			return True
		return False

	def move_right(self):
		i, k = self.find_number(0)
		if k > 0 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i][k - 1]
			self.tiles[i][k - 1] = 0
			self.tiles_list[i][k] = self.tiles_list[i][k - 1]
			self.tiles_list[i][k - 1] = None
			self.tiles_list[i][k].change_x = self.tile_speed
			self.tile_moving = { 'dest_y': self.tiles_list[i][k].center_y, 'dest_x': self.tiles_list[i][k].center_x  + self.tile_travel_distance, 'sprite': self.tiles_list[i][k]}
			return True
		return False

	def move_up(self):
		i, k = self.find_number(0)
		if i < self.n - 1 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i + 1][k]
			self.tiles[i + 1][k] = 0
			self.tiles_list[i][k] = self.tiles_list[i + 1][k]
			self.tiles_list[i + 1][k] = 0
			self.tiles_list[i][k].change_y = self.tile_speed
			self.tile_moving = { 'dest_y': self.tiles_list[i][k].center_y + self.tile_travel_distance, 'dest_x': self.tiles_list[i][k].center_x, 'sprite': self.tiles_list[i][k]}
			return True
		return False
	
	def move_down(self):
		i, k = self.find_number(0)
		if i > 0 and not self.tile_moving:
			self.tiles[i][k] = self.tiles[i - 1][k]
			self.tiles[i - 1][k] = 0
			self.tiles_list[i][k] = self.tiles_list[i - 1][k]
			self.tiles_list[i - 1][k] = 0
			self.tiles_list[i][k].change_y = -1 * self.tile_speed
			self.tile_moving = { 'dest_y': self.tiles_list[i][k].center_y - self.tile_travel_distance, 'dest_x': self.tiles_list[i][k].center_x, 'sprite': self.tiles_list[i][k]}
			return True
		return False

	def check_end(self):
		i = 0
		while i < self.n:
			k = 0
			while k < self.n:
				if k == self.n - 1 and i == self.n - 1 and self.tiles[i][k] == 0:
					return True
				if self.tiles[i][k] != i * self.n + k + 1:
					return False
				k += 1
			i += 1
		return False


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