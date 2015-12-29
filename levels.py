import pygame
import xml.etree.ElementTree

import sprites
from gamelib import vector

def _makeVec(x, sep="x"):
	return vector.Vector(int(i) for i in x.split(sep))

class SpritesFactory(object):
	def __init__(self, game):
		self.game=game

	def makePlayer(self, pos, scale=1, offset=vector.Vector(0, 0)):
		sprite=sprites.Player(self.game, pos*scale+offset, scale)
		self.game.all.add(sprite)
		return sprite

	def makeWall(self, pos, size, scale=1, offset=vector.Vector(0, 0)):
		sprite=sprites.Wall(self.game, pos*scale+offset, size*scale)
		self.game.all.add(sprite)
		self.game.walls.add(sprite)
		return sprite

	def makeEnemy(self, pos1, pos2, speed, scale=1, offset=vector.Vector(0, 0)):
		sprite=sprites.Enemy(self.game, pos1*scale+offset, pos2*scale+offset, speed*scale, scale)
		self.game.all.add(sprite)
		self.game.enemies.add(sprite)
		return sprite

	def makeFood(self, pos, scale=1, offset=vector.Vector(0, 0)):
		sprite=sprites.Food(self.game, pos*scale+offset, scale)
		self.game.all.add(sprite)
		self.game.food.add(sprite)
		return sprite

	def makeTarget(self, pos, size, scale=1, offset=vector.Vector(0, 0)):
		sprite=sprites.Target(self.game, pos*scale+offset, size*scale)
		self.game.all.add(sprite)
		self.game.targets.add(sprite)
		return sprite

	def loadLevel(self, path):
		screenRect=self.game.screen.get_rect()
		tree=xml.etree.ElementTree.parse(path)
		root=tree.getroot()
		# level.name=root.get("name")
		size=_makeVec(root.get("size"))

		scale=min(screenRect.width/size.x,
		          screenRect.height/size.y)
		levelRect=pygame.Rect((0, 0), size*scale)
		levelRect.center=screenRect.center
		offset=vector.Vector(levelRect.topleft)

		self.game.player=self.makePlayer(_makeVec(root.get("playerPos")), scale, offset)
		self.game.orig_player_pos=self.game.player.rect.center

		for element in root.iterfind("wall"):
			self.makeWall(_makeVec(element.get("pos")),
			              _makeVec(element.get("size")),
			              scale, offset)
		for element in root.iterfind("enemy"):
			self.makeEnemy(_makeVec(element.get("pos1")),
			               _makeVec(element.get("pos2")),
			               int(element.get("speed")),
			               scale, offset)
		for element in root.iterfind("food"):
			self.makeFood(_makeVec(element.get("pos")),
			              scale, offset)
		for element in root.iterfind("target"):
			self.makeTarget(_makeVec(element.get("pos")),
			              _makeVec(element.get("size")),
			              scale, offset)
