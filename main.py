import os

from game import pygame, Game

pygame.init()

class Manager(object):
	def __init__(self, screenSize=(640, 480), winFlags=0):
		self.screen=pygame.display.set_mode(screenSize, winFlags)

		self.game=Game(self, os.path.join("resources", "levels"))

	def main(self):
		self.game.main()

if __name__ == '__main__':
	m=Manager(pygame.display.list_modes()[0], pygame.FULLSCREEN)    #automatically launches it on fullscreen mode
	m.main()