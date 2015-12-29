import os, sys

from game import pygame, Game

pygame.init()

class Manager(object):
	def __init__(self, screenSize=(1234, 876), winFlags=0):
		self.screen=pygame.display.set_mode(screenSize, winFlags)

		self.game=Game(self, "resources/levels")

	def main(self):
		self.game.main()

if __name__ == '__main__':
	m=Manager(winFlags=pygame.FULLSCREEN)
	m.main()