import arcade as ar
import os
from sources.grid import create_grid_blank
from sources.astar import astar_path

GRID_W = 25
GRID_H = 25

TILE_SIZE = 32
TILE_COLOR_EMPTY = ar.color.AMAZON
TILE_COLOR_FULL = ar.color.ORANGE_PEEL
TILE_TRACE = ar.color.PINK_LACE

A_STAR_H = 'euclid'

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
		self.astar_trace_speed = 60
		self.astar_trace_shadow = list()
		self.astar_draw = False
		self.astar_heuristic = A_STAR_H

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
				shape = self.create_square_sprite(i, k, ar.color.ORANGE_PEEL)
				shape.alpha = alpha
				shape.center_x = x
				shape.center_y = y
				self.grid_list.append(shape)
	
	def create_square_sprite(self, i, k, color):
		x = self.tile_size // 2 + self.tile_size * k
		y = self.tile_size // 2 + self.tile_size * i
		new = ar.SpriteSolidColor(self.tile_size, self.tile_size, color)
		new.center_x = x
		new.center_y = y
		return new

	def on_draw(self):
		ar.start_render()
		self.grid_list.draw()
		self.startSprite.draw()
		self.endSprite.draw()
		if 0 < self.astar_trace_number <= self.astar_trace_len:
			self.draw_trace()
	
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
		elif key == ar.key.T:
			if self.astar_trace_animate:
				self.astar_trace_animate = 0
				ar.unschedule(self.increase_step_trace)
				print("Trace Off")
			else:
				self.astar_trace_animate = 1
				ar.schedule(self.increase_step_trace, 1/self.astar_trace_speed)
				print("Trace On")
		elif key == ar.key.KEY_1:
			self.astar_heuristic = 'manhattan'
			print(f"Heuristic set to {self.astar_heuristic}")
		elif key == ar.key.KEY_2:
			self.astar_heuristic = 'euclid'
			print(f"Heuristic set to {self.astar_heuristic}")

	def astar_find_path(self):
		self.astar_path = None
		self.astar_trace = None
		self.astar_trace_number = 0
		self.astar_trace_len = 0
		self.astar_trace_animate = 0
		self.astar_trace_shadow = ar.SpriteList()
		self.astar_draw = False
		suc, self.astar_path, self.astar_trace = astar_path(self.grid, self.start, self.end, self.astar_heuristic)
		self.astar_draw = False
		self.astar_trace_len = len(self.astar_trace)
		if not suc:
			print("A* error")
			exit()
		print(self.astar_path)
	
	def draw_trace(self):
		if self.astar_trace:
			self.astar_trace_shadow.draw()
			self.draw_one_path(self.astar_trace[self.astar_trace_number - 1], ar.color.PINK_PEARL)
	
	def draw_one_path(self, path, color):
		points = list()
		for p in path:
			n = (p[0] * self.tile_size + self.tile_size / 2, p[1] * self.tile_size + self.tile_size / 2)
			points.append(n)
		ar.draw_line_strip(points, color, 5)
	
	def increase_step_trace(self, dump):
		if self.astar_trace_number < self.astar_trace_len:
			tmp = self.astar_trace[self.astar_trace_number - 1][-1]
			new = self.create_square_sprite(tmp[1], tmp[0], ar.color.PINK_LACE)
			self.astar_trace_shadow.append(new)
			self.astar_trace_number += 1

def run_program():
	window = PlainGrid(GRID_W, GRID_H, TILE_SIZE)
	window.setup()
	ar.run()

if __name__ == "__main__":
	run_program()