import arcade as ar
import os
import random

#Settings
WIN_W = 1000
WIN_H = 1000
TITLE = "Balls"
BALL_COUNT = 10
BALL_RATIO = 0.5
GRAVITY = 1
GRASS_FIT = int(WIN_W / (200 * BALL_RATIO))

#My Game
class BallsGame(ar.Window):
	def __init__(self):
		super().__init__(WIN_W, WIN_H, TITLE)
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)
		self.balls_list = None
		self.walls_list = None
		self.engine = None
		ar.set_background_color(ar.color.BLACK)
	
	def setup(self, balls_count):
		self.balls_list = ar.SpriteList()
		self.walls_list = ar.SpriteList()
		for i in range(balls_count):
			new = ar.Sprite("resources/football_color.png", BALL_RATIO)
			x = random.randint(100, WIN_W - 100)
			y = random.randint(300, WIN_H - 100)
			n = 0
			while n < len(self.balls_list):
				if self.balls_list[n].center_x in range(x - 100, x + 100) and self.balls_list[n].center_y in range(y - 100, y + 100):
					x = random.randint(100, WIN_W - 100)
					y = random.randint(300, WIN_H - 100)
					n = 0
				else:
					n += 1
			new.center_x = x
			new.center_y = y
			new.change_x = 1
			new.change_y = 1
			print(f"Created Ball {i}")
			self.balls_list.append(new)
		for i in range(GRASS_FIT):
			wall = ar.Sprite('resources/grass_tile.png', BALL_RATIO)
			wall.center_y = 50
			wall.center_x = 50 + i * 200 * BALL_RATIO
			wall.change_x = 0
			wall.change_y = 0
			self.walls_list.append(wall)
		self.engine = ar.PhysicsEnginePlatformer(self.balls_list, self.walls_list, GRAVITY)

	def on_draw(self):
		ar.start_render()
		self.balls_list.draw()
		self.walls_list.draw()

	def on_update(self, delta_time):
		self.balls_list.update()
		self.walls_list.update()
		self.engine.update()

# class Ball(ar.Sprite):
# 	def __init__(self):
# 		se
# 		self.radius = 10
# 		self.pos_x = random.randint(0 + self.radius, WIN_W - self.radius)
# 		self.pos_y = random.randint(0 + self.radius, WIN_H - self.radius)
# 		self.delta_x = delta_x
# 		self.delta_y = delta_y
	
# 	def move(self):
# 		self.pos_x += self.delta_x
# 		self.pos_y += self.delta_y
	
# 	def draw(self):
# 		ar.draw_circle_filled(self.pos_x, self.pos_y, self.radius, self.color)

def main():
	"""Main Method"""
	window = BallsGame()
	window.setup(BALL_COUNT)
	ar.run()

if __name__ == "__main__":
	main()