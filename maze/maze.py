import arcade as ar
import os
from sources.grid import create_maze_depthfirst_multipath, find_end_xy, find_start_xy
from sources.bfs import bfs_path
from sources.astar import astar_path

# Settings
SPRITE_SIZE = 8
SPRITE_SCALE = SPRITE_SIZE / 128


MAZE_W = 81
MAZE_H = 81
WIN_W = int(MAZE_W * SPRITE_SIZE)
WIN_H = int(MAZE_H * SPRITE_SIZE)

MAZE_PATHS = 3

class MazeGame(ar.Window):
	def __init__(self, win_w, win_h, maze_w, maze_h):
		super().__init__(win_w, win_h, f"Maze {maze_w}x{maze_h}")
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)
		self.maze_w = maze_w
		self.maze_h = maze_h
		self.maze = None
		self.wall_list = None
		self.start_end = None
		self.path = dict()
		self.path_draw = dict()
		self.path_index_bfs = 0
		self.path_index_bfs_change = 0
		self.anim_speed = 1
		self.playback_path = False
		self.astar_trace = None
		self.astar_trace_number = 0
		self.astar_trace_len = 0
		self.astar_trace_animate = 0
		self.astar_trace_speed = 5
		self.astar_trace_shadow = list()
	
	def setup(self):
		ar.set_background_color(ar.color.BRITISH_RACING_GREEN)
		self.maze = create_maze_depthfirst_multipath(self.maze_w, self.maze_h, MAZE_PATHS)
		self.wall_list = ar.SpriteList()
		self.start_end = ar.SpriteList()
		for row in range(self.maze_h):
			for column in range(self.maze_w):
				if self.maze[row][column] == 1:
					wall = ar.Sprite(":resources:images/tiles/brickBrown.png", SPRITE_SCALE)
					wall.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
					wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
					self.wall_list.append(wall)
				elif self.maze[row][column] == 2:
					start = ar.Sprite(":resources:images/tiles/brickGrey.png", SPRITE_SCALE)
					start.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
					start.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
					self.start_end.append(start)
				elif self.maze[row][column] == 3:
					end = ar.Sprite(":resources:images/tiles/signExit.png", SPRITE_SCALE)
					end.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
					end.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
					self.start_end.append(end)
		suc, path = bfs_path(self.maze, find_start_xy(self.maze, self.maze_w, self.maze_h), find_end_xy(self.maze, self.maze_w, self.maze_h))
		if suc:
			self.add_path(path, 'bfs')
			self.path_draw['bfs'] = False
		else:
			print("BFS error")
			exit()
		suc, apath, self.astar_trace = astar_path(self.maze, find_start_xy(self.maze, self.maze_w, self.maze_h), find_end_xy(self.maze, self.maze_w, self.maze_h))
		if suc:
			self.add_path(apath, 'astar')
			self.path_draw['astar'] = False
			self.astar_trace_len = len(self.astar_trace)
		else:
			print("A* error")
			exit()
		print("Setup Done")
		print(f"A* trace len: {self.astar_trace_len}")

	def on_draw(self):
		ar.start_render()
		self.wall_list.draw()
		self.start_end.draw()
		self.draw_all_paths()
		if self.path_index_bfs:
			self.draw_steps_path('bfs')
		if 0 < self.astar_trace_number < self.astar_trace_len:
			self.draw_trace()

	def on_update(self, delta_time):
		if 'bfs' in self.path.keys():
			if self.path_index_bfs_change < 0 and self.path_index_bfs >= self.path_index_bfs_change * -1:
				self.path_index_bfs += self.path_index_bfs_change
			elif self.path_index_bfs_change > 0 and self.path_index_bfs < len(self.path['bfs']) - self.path_index_bfs_change:
				self.path_index_bfs += self.path_index_bfs_change
		if self.astar_trace_number == self.astar_trace_len and self.astar_trace_animate:
			self.astar_trace_animate = 0
			print("Trace reached the end")
			ar.unschedule(self.increase_step_trace)
			self.path_draw['astar'] = True


	def on_key_release(self, symbol, modifier):
		if symbol == ar.key.KEY_1:
			if self.path_draw['bfs']:
				self.path_draw['bfs'] = False
			else:
				self.path_draw['bfs'] = True
		elif symbol == ar.key.KEY_2:
			if self.path_draw['astar']:
				self.path_draw['astar'] = False
			else:
				self.path_draw['astar'] = True
		elif symbol == ar.key.RIGHT or symbol == ar.key.LEFT:
				self.path_index_bfs_change = 0
		elif symbol == ar.key.SPACE:
			if self.path_index_bfs_change:
				self.path_index_bfs_change = 0
			else:
				self.path_index_bfs_change = self.anim_speed
		elif symbol == ar.key.T:
			if self.astar_trace_animate:
				self.astar_trace_animate = 0
				ar.unschedule(self.increase_step_trace)
				print("Trace Off")
			else:
				self.astar_trace_animate = 1
				ar.schedule(self.increase_step_trace, 1/self.astar_trace_speed)
				print("Trace On")
		elif symbol == ar.key.R:
			self.astar_trace_number = 0

	def on_key_press(self, symbol, modifier):
		if symbol == ar.key.RIGHT:
			self.path_index_bfs_change = self.anim_speed
		elif symbol == ar.key.LEFT:
			self.path_index_bfs_change = -1 * self.anim_speed
		elif symbol == ar.key.NUM_ADD:
			self.astar_trace_speed += 1
			print(f"Trace animation refresh rate set to 1/{self.astar_trace_speed}")
			if self.astar_trace_animate:
				ar.unschedule(self.increase_step_trace)
				ar.schedule(self.increase_step_trace, 1/self.astar_trace_speed)
		elif symbol == ar.key.NUM_SUBTRACT and self.astar_trace_speed > 1:
			self.astar_trace_speed -= 1
			print(f"Trace animation refresh rate set to 1/{self.astar_trace_speed}")
			if self.astar_trace_animate:
				ar.unschedule(self.increase_step_trace)
				ar.schedule(self.increase_step_trace, 1/self.astar_trace_speed)

	def on_mouse_release(self, x, y, button, modifier):
		pos_x = int(x / SPRITE_SIZE)
		pos_y = int(y / SPRITE_SIZE)
		if button == ar.MOUSE_BUTTON_LEFT:
			print(f"Current position [{pos_x}, {pos_y}]")

	def add_path(self, path, name):
		self.path[name] = path

	def draw_one_path(self, path, color):
		points = list()
		for p in path:
			n = (p[0] * SPRITE_SIZE + SPRITE_SIZE / 2, p[1] * SPRITE_SIZE + SPRITE_SIZE / 2)
			points.append(n)
		ar.draw_line_strip(points, color, 5)

	def draw_all_paths(self):
		if len(self.path):
			colors = [ar.color.BLUE, ar.color.YELLOW, ar.color.RED]
			ci = 0
			for key in self.path_draw:
				if self.path_draw[key]:
					self.draw_one_path(self.path[key], colors[ci])
					ci = (ci + 1) % len(colors)

	def draw_steps_path(self, key):
		points = list()
		for step in self.path[key][:self.path_index_bfs + 1]:
			n = (step[0] * SPRITE_SIZE + SPRITE_SIZE / 2, step[1] * SPRITE_SIZE + SPRITE_SIZE / 2)
			points.append(n)
		ar.draw_line_strip(points, ar.color.ORANGE_PEEL, 3)

	def increase_step_trace(self, dump):
		if self.astar_trace_number < self.astar_trace_len:
			tmp = self.astar_trace[self.astar_trace_number - 1]
			for step in range(len(tmp)):
				if not tmp[step] in self.astar_trace_shadow:
					if self.astar_trace_shadow == []:
						self.astar_trace_shadow.append(tmp[step])
					elif step != 0:
						self.astar_trace_shadow.insert(self.astar_trace_shadow.index(tmp[step - 1]), tmp[step])
			self.astar_trace_number += 1
		print(f"Trace on {self.astar_trace_number}")

	def draw_trace(self):
		if self.astar_trace:
			self.draw_one_path(self.astar_trace_shadow, ar.color.PINK_LACE)
			self.draw_one_path(self.astar_trace[self.astar_trace_number - 1], ar.color.PINK_PEARL)
			


def main():
	window = MazeGame(WIN_W, WIN_H, MAZE_W, MAZE_H)
	window.setup()
	ar.run()

if __name__ == "__main__":
	main()