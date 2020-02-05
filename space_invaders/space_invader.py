import pygame as pg
from random import randint

pg.init()
win_width = 800
win_height = 600
root = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Jiri's fun stuff")

def get_distance(p1, p2):
	return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

class Player():
	def __init__(self, win_width, win_height):
		self.img = pg.image.load('spaceship2.png')
		self.x = win_width / 2 - 32
		self.y = win_height - 164
		self.xmax = win_width - 64
		self.ymax = win_height - 64
		self.x_spd = 0
		self.y_spd = 0
		self.speed = 0.2
		self.score = 0
	
	def draw(self):
		root.blit(self.img, (int(self.x), int(self.y)))
	
	def move(self):
		self.x += self.x_spd
		self.y += self.y_spd
		if self.x < 0:
			self.x = 0
		elif self.x > self.xmax:
			self.x = win_width - 64
		if self.y < 0:
			self.y = 0
		elif self.y > self.ymax:
			self.y = win_height - 64
		self.draw()

class Enemy():

	def __init__(self):
		self.img = pg.image.load('spooky.png')
		self.dead_img = pg.image.load('flame.png')
		self.respawn()

	def draw(self):
		if self.alive:
			root.blit(self.img, (int(self.x), int(self.y)))
		else:
			if self.counter:
				explosion = pg.transform.rotate(self.dead_img, randint(-180, 180))
				root.blit(explosion, (int(self.x), int(self.y)))
				self.counter -= 1
			else:
				self.respawn()

	def move(self, xmax, ymax):
		if self.alive:
			self.x += self.x_spd
			if not self.y_spd:
				direction = randint(-1, 1)
				self.y_spd =[direction] * 500
			self.y +=  self.y_spd.pop(0) * self.speed * 0.5
			if self.x < 0:
				self.x = 0
				self.x_spd = self.speed
			elif self.x > xmax:
				self.x = xmax
				self.x_spd = -1 * self.speed
			if self.y < 0:
				self.y = 0
			elif self.y > ymax:
				self.y = ymax
		self.draw()
	
	def die(self):
		self.x_spd = 0
		self.speed = 0
		self.alive = False
	
	def respawn(self):
		self.alive = True
		self.x = randint(0, win_width - 64)
		self.y = randint(0, win_height - 350)
		self.speed = 0.1
		self.y_spd = list()
		self.x_spd = self.speed
		self.counter = 500

class Projectile():
	def __init__(self):
		self.org_img = pg.image.load('rocket.png')
		self.img = pg.transform.rotate(self.org_img, 45)
		self.x = 0
		self.y = 0
		self.speed = 0.35
		self.active = False
		self.side = True
	
	def action(self, window=root):
		if self.active:
			self.move()
			window.blit(self.img, (int(self.x), int(self.y)))

	def shoot(self, org_x, org_y):
		if not self.active:
			if self.side:
				self.x = org_x + 5
				self.side = False
			else:
				self.x = org_x + 38
				self.side = True
			self.y = org_y + 32
			self.active = True
	
	def move(self):
		self.y -= self.speed
		if self.y < -12:
			self.active = False
	

monster = Enemy()
proj = Projectile()
player = Player(win_width, win_height)

#scoreboard
font = pg.font.Font('font1.ttf', 32)


play = True
while play:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			play = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_LEFT:
				player.x_spd = -player.speed
			if event.key == pg.K_RIGHT:
				player.x_spd = +player.speed
			if event.key == pg.K_UP:
				player.y_spd = -player.speed
			if event.key == pg.K_DOWN:
				player.y_spd = player.speed
			if event.key == pg.K_SPACE:
				proj.shoot(player.x, player.y)
		if event.type == pg.KEYUP:
			if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
				player.x_spd = 0
			if event.key == pg.K_UP or  event.key == pg.K_DOWN:
				player.y_spd = 0
			if event.key == pg.K_ESCAPE:
				pg.quit()
				exit()	
	root.fill((0, 0, 0))

	#Player movement
	
	if proj.active and get_distance((monster.x + 32, monster.y + 32), (proj.x + 6, proj.y)) < 30:
		proj.active = False
		monster.die()
		player.score += 1
	monster.move(win_width - 64, win_height - 64)
	proj.action(root)
	player.move()

	#Score
	text = font.render(f"Score: {player.score}", True, (255, 0, 0))
	textrec = text.get_rect()
	textrec.center = (int(win_width / 2), int(win_height - 32))
	root.blit(text, textrec)
	pg.display.update()