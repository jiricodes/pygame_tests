import arcade as ar
import os
from sources.grid import create_grid_blank
from sources.astar import astar_path

GRID_W = 10
GRID_H = 10

TILE_SIZE = 32
TILE_COLOR_EMPTY = ar.color.AMAZON
TILE_COLOR_FULL = ar.color.ORANGE_PEEL

A_STAR_H = 'manhattan'

class PlainGrid(ar.Window):
	def __init__(self, width, height, tile_size):
		super().__init__(width * tile_size, height * tile_size, title="Plain Grid")
		self.w = width
		self.h = height
		self.tile_size = tile_size
		self.grid = None
		self.grid_list = None
		self.lifted = False
		self.start = [0, 0]
		self.startSprite = None
		self.end = [self.w - 1, self.h - 1]
		self.endSprite = None
		self.astar_path = None
		self.astar_trace = None
		self.astar_trace_number = 0
		self.astar_trace_len = 0
		self.astar_trace_animate = 0
		self.astar_trace_speed = 20
		self.astar_trace_shadow = list()
		self.astar_show_values = False
		self.astar_draw = False

	def __str__(self):
		s = f"PlainGrid {self.w}x{self.h}\n"
		for row in self.grid[::-1]:
			for item in row:
				s += f" {item} |"
			s+= "\n"
		return s

	def setup(self):
		ar.set_background_color(ar.color.AMAZON)
		self.grid = create_grid_blank(self.w, self.h)
		self.grid[self.start[1]][self.start[0]] = 2
		self.grid[self.end[1]][self.end[0]] = 3
		self.startSprite = ar.Sprite(":resources:images/tiles/brickGrey.png", self.tile_size / 128)
		self.startSprite.center_y = self.tile_size // 2 + self.tile_size * self.start[1]
		print(self.startSprite.center_y)
		self.startSprite.center_x = self.tile_size // 2 + self.tile_size * self.start[0]
		print(self.startSprite.center_x)
		self.endSprite = ar.Sprite(":resources:images/tiles/signExit.png", self.tile_size / 128)
		self.endSprite.center_y = self.tile_size // 2 + self.tile_size * self.end[1]
		self.endSprite.center_x = self.tile_size // 2 + self.tile_size * self.end[0]
		self.make_grid_shapes()
		print(self.__str__())
	
	def make_grid_shapes(self):
		self.grid_list = ar.SpriteList()
		for i in range(self.h):
			for k in range(self.w):
				if self.grid[i][k] == 1:
					alpha = 255
				else:
					alpha = 0
				x = self.tile_size // 2 + self.tile_size * k
				y = self.tile_size // 2 + self.tile_size * i
				shape = self.create_square_sprite(i, k)
				shape.alpha = alpha
				shape.center_x = x
				shape.center_y = y
				self.grid_list.append(shape)
	
	def create_square_sprite(self, i, k):
		x = self.tile_size // 2 + self.tile_size * k
		y = self.tile_size // 2 + self.tile_size * i
		new = ar.SpriteSolidColor(self.tile_size, self.tile_size, TILE_COLOR_FULL)
		new.center_x = x
		new.center_y = y
		return new

	def on_draw(self):
		ar.start_render()
		self.grid_list.draw()
		self.startSprite.draw()
		self.endSprite.draw()
	
	def on_update(self,deltatime):
		self.grid_list.update()

	def on_mouse_press(self, x, y, button, modifiers):
		i = y // self.tile_size
		k = x // self.tile_size
		if i < self.h and k < self.w:
			index = i * self.h + k
			if button == ar.MOUSE_BUTTON_LEFT and self.grid[i][k] == 0 and not self.lifted:
				self.grid[i][k] = 1
				self.grid_list[index].alpha = 255
			elif button == ar.MOUSE_BUTTON_RIGHT and self.grid[i][k] == 1 and not self.lifted:
				self.grid[i][k] = 0
				self.grid_list[index].alpha = 0
			elif button == ar.MOUSE_BUTTON_LEFT and (self.grid[i][k] == 2 or self.grid[i][k] == 3) and not self.lifted:
				self.pickup_sprite(i, k)
				self.grid_list[index].alpha = 0
			elif button == ar.MOUSE_BUTTON_LEFT and (self.grid[i][k] == 0 or self.grid[i][k] == 1) and self.lifted:
				self.drop_lifted(i, k)
				self.grid_list[index].alpha = 0
	
	def on_mouse_motion(self, x, y, dx, dy):
		if self.lifted:
			self.lifted.center_y = y
			self.lifted.center_x = x

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		i = y // self.tile_size
		k = x // self.tile_size
		if 0 <= i < self.h and 0 <= k < self.w:
			index = i * self.h + k
			if button == ar.MOUSE_BUTTON_LEFT and self.grid[i][k] == 0 and not self.lifted:
				self.grid[i][k] = 1
				self.grid_list[index].alpha = 255
			elif button == ar.MOUSE_BUTTON_RIGHT and self.grid[i][k] == 1 and not self.lifted:
				self.grid[i][k] = 0
				self.grid_list[index].alpha = 0
	
	def pickup_sprite(self, i, k):
		if not self.lifted:
			if self.grid[i][k] == 2:
				self.lifted = self.startSprite
			elif self.grid[i][k] == 3:
				self.lifted = self.endSprite
			self.set_mouse_visible(False)
			self.grid[i][k] = 0

	def drop_lifted(self, i, k):
		if self.lifted:
			self.lifted.center_x = self.tile_size // 2 + self.tile_size * k
			self.lifted.center_y = self.tile_size // 2 + self.tile_size * i
			if self.lifted.center_x == self.startSprite.center_x and self.lifted.center_y == self.startSprite.center_y:
				self.grid[i][k] = 2
				self.start = [k, i]
			elif self.lifted.center_x == self.endSprite.center_x and self.lifted.center_y == self.endSprite.center_y:
				self.grid[i][k] = 3
				self.end = [k, i]
			self.lifted = None
			self.set_mouse_visible(True)
	
	def on_key_release(self, key, mod):
		if key == ar.key.SPACE:
			print(self.__str__())
		elif key == ar.key.A:
			self.astar_find_path()

	def astar_find_path(self):
		suc, self.astar_path, self.astar_trace = astar_path(self.grid, self.start, self.end, A_STAR_H)
		self.astar_draw = False
		self.astar_trace_len = len(self.astar_trace)
		if not suc:
			print("A* error")
			exit()
		print(self.astar_path)

def run_program():
	window = PlainGrid(GRID_W, GRID_H, TILE_SIZE)
	window.setup()
	ar.run()

if __name__ == "__main__":
	run_program()