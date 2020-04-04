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
		self.path_draw = True
	
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
		suc, apath = astar_path(self.maze, find_start_xy(self.maze, self.maze_w, self.maze_h), find_end_xy(self.maze, self.maze_w, self.maze_h))
		if suc:
			self.add_path(apath, 'astar')

	def on_draw(self):
		ar.start_render()
		self.wall_list.draw()
		self.start_end.draw()
		if self.path_draw:
			self.draw_path()
	
	def on_update(self, delta_time):
		pass
	
	def on_key_release(self, symbol, modifier):
		if symbol == ar.key.KEY_1:
			self.path_draw = False
		elif symbol == ar.key.KEY_2:
			self.path_draw = True
	
	def on_mouse_release(self, x, y, button, modifier):
		pos_x = int(x / SPRITE_SIZE)
		pos_y = int(y / SPRITE_SIZE)
		if button == ar.MOUSE_BUTTON_LEFT:
			print(f"Current position [{pos_x}, {pos_y}]")

	def add_path(self, path, name):
		self.path[name] = path

	def draw_path(self):
		if len(self.path):
			for key in self.path:
				points = list()
				for p in self.path[key]:
					n = (p[0] * SPRITE_SIZE + SPRITE_SIZE / 2, p[1] * SPRITE_SIZE + SPRITE_SIZE / 2)
					points.append(n)
				ar.draw_line_strip(points, ar.color.BLUE_BELL, 5)

def main():
	window = MazeGame(WIN_W, WIN_H, MAZE_W, MAZE_H)
	window.setup()
	ar.run()

if __name__ == "__main__":
	main()