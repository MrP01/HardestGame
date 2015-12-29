import os
import sys

from gamelib import control
from levels import *

class Game(control.SpriteControl):
	bgColor=(255, 255, 255)
	fps=24
	def __init__(self, manager, levelDir):
		bg=pygame.Surface(manager.screen.get_size())
		bg.fill(Game.bgColor)
		control.SpriteControl.__init__(self, manager, bg)

		self.clock=pygame.time.Clock()
		self.pressedKeys=[]

		self.enemies=pygame.sprite.Group()
		self.walls=pygame.sprite.Group()
		self.food=pygame.sprite.Group()
		self.targets=pygame.sprite.Group()
		self.player=None
		self.orig_player_pos=vector.Vector(0, 0)

		self.levelFiles=[]
		self.currentLevel=None
		self.currentLevelIndex=0
		for file in sorted(os.listdir(levelDir)):
			self.levelFiles.append(os.path.join(levelDir, file))

		self.score=0
		self.scoreBoard=sprites.Score(self)

		self.factory=SpritesFactory(self)

	def setLevel(self, level):
		self.all.empty()
		self.all.add(self.scoreBoard)
		self.enemies.empty()
		self.walls.empty()
		self.food.empty()
		self.targets.empty()
		self.factory.loadLevel(level)

	def restartLevel(self):
		self.player.rect.center=self.orig_player_pos

	def startLevels(self):
		self.currentLevelIndex=0
		self.setLevel(self.levelFiles[0])

	def nextLevel(self):
		if any(food.alive() for food in self.food):
			print("Cannot load next level, you have to collect all food")
			return
		try:
			self.currentLevelIndex+=1
			self.setLevel(self.levelFiles[self.currentLevelIndex])
		except IndexError:
			print("Congratulations, you won!")
			sys.exit()

	def main(self):
		self.startLevels()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return
			self.pressedKeys=pygame.key.get_pressed()
			self.updateScreen()
			self.clock.tick(Game.fps)