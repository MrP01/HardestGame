import pygame

from gamelib import vector

class Player(pygame.sprite.Sprite):
	size=vector.Vector(16, 16)
	orig_image=pygame.image.load("resources/img/Player.png")
	orig_speed=5
	def __init__(self, game, pos, sizeScale=1):
		pygame.sprite.Sprite.__init__(self)
		self.game=game
		self.image=Player.orig_image
		self.rect=self.image.get_rect(center=pos)
		self.speed=Player.orig_speed
		self.scale(sizeScale)
	
	def scale(self, scale):
		self.image=pygame.transform.scale(Player.orig_image, Player.size*scale)
		self.rect=self.image.get_rect(center=self.rect.center)
		self.speed=Player.orig_speed*scale

	def update(self):
		if self.game.pressedKeys[pygame.K_UP]:
			self.move(0, -self.speed)
		elif self.game.pressedKeys[pygame.K_DOWN]:
			self.move(0, self.speed)
		if self.game.pressedKeys[pygame.K_RIGHT]:
			self.move(self.speed, 0)
		elif self.game.pressedKeys[pygame.K_LEFT]:
			self.move(-self.speed, 0)

	def move(self, x, y):
		self.rect.move_ip(x, y)
		for wall in pygame.sprite.spritecollide(self, self.game.walls, False):
			if x > 0: self.rect.right=wall.rect.left
			elif x < 0: self.rect.left=wall.rect.right
			if y > 0: self.rect.bottom=wall.rect.top
			elif y < 0: self.rect.top=wall.rect.bottom

class Enemy(pygame.sprite.Sprite):
	size= vector.Vector(16, 16)
	orig_image=pygame.image.load("resources/img/Enemy.png")
	toP1, toP2 = 1, 2
	def __init__(self, game, pos1, pos2, speed, sizeScale=1):
		pygame.sprite.Sprite.__init__(self)
		self.game=game
		self.image=pygame.transform.scale(Enemy.orig_image, Enemy.size*sizeScale)
		self.rect=self.image.get_rect(center=pos1)
		self.pos1, self.pos2 = vector.Vector(pos1), vector.Vector(pos2)
		self.dist=(self.pos2-self.pos1).length()
		self.speed=speed
		self.direction=(self.pos2-self.pos1).normalized()
		self.state=Enemy.toP2

	def update(self):
		self.rect.move_ip(self.direction*self.speed)
		if self.state == Enemy.toP2 and (vector.Vector(self.rect.center)-self.pos1).length() >= self.dist:
			self.direction*=-1
			self.state=Enemy.toP1
		elif self.state == Enemy.toP1 and (vector.Vector(self.rect.center)-self.pos2).length() >= self.dist:
			self.direction*=-1
			self.state=Enemy.toP2
		if self.rect.colliderect(self.game.player):
			self.game.restartLevel()

class Wall(pygame.sprite.Sprite):
	color=(0, 0, 0)
	def __init__(self, game, pos, size):
		pygame.sprite.Sprite.__init__(self)
		self.game=game
		self.image=pygame.Surface(size)
		self.rect=self.image.get_rect(topleft=pos)

		self.image.fill(Wall.color)

class Food(pygame.sprite.Sprite):
	size= vector.Vector(8, 8)
	orig_image=pygame.image.load("resources/img/Food.png")
	def __init__(self, game, pos, sizeScale=1):
		pygame.sprite.Sprite.__init__(self)
		self.game=game
		self.image=pygame.transform.scale(Food.orig_image, Food.size*sizeScale)
		self.rect=self.image.get_rect(center=pos)

	def update(self):
		if self.rect.colliderect(self.game.player):
			self.kill()

class Target(pygame.sprite.Sprite):
	color=(150, 250, 255)
	def __init__(self, game, pos, size):
		pygame.sprite.Sprite.__init__(self)
		self.game=game
		self.image=pygame.Surface(size)
		self.image.set_alpha(200)
		self.rect=self.image.get_rect(center=pos)

		self.image.fill(Target.color)

	def update(self):
		if self.rect.colliderect(self.game.player):
			self.game.nextLevel()

class Score(pygame.sprite.Sprite):
	color=(0, 0, 0)
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		self.game=game
		self.font = pygame.font.Font(None, 24)
		self.lastscore = -1
		self.image=None
		self.update()
		self.rect = self.image.get_rect().move(30, 30)

	def update(self):
		if self.game.score != self.lastscore:
			self.lastscore = self.game.score
			msg = "Score: {}".format(self.game.score)
			self.image = self.font.render(msg, 0, Score.color)
