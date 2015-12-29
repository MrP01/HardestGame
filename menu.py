import pygame
from pygame.sprite import Sprite, Group

from gamelib import control


class MenuEntry(Sprite):
	defaultColor=(0, 0, 0)
	def __init__(self, menu, text, action, color=defaultColor):
		Sprite.__init__(self)
		self.menu=menu
		self.font=pygame.font.SysFont("Liberation sans ms", 24)
		self.image=self.font.render(text, True, color)
		self.rect=self.image.get_rect()
		self.action=action

	def checkPressed(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.action()

class Menu(control.SpriteControl):
	def __init__(self, manager, background, entries):
		control.SpriteControl.__init__(self, manager, background)
		self.entries=Group()

	def main(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					break
				elif event.type == pygame.MOUSEBUTTONDOWN:
					for entry in self.entries:
						entry.checkPressed()
			self.updateScreen()
