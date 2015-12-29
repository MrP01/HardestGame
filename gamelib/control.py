import pygame

class Control(object):
	def __init__(self, manager):
		self.manager=manager

	@property
	def screen(self):
		return self.manager.screen

	def main(self):
		#Here goes main loop
		pass

class SpriteControl(Control):
	def __init__(self, manager, background):
		Control.__init__(self, manager)
		self.all=pygame.sprite.RenderUpdates()
		self.background=background
		self.screen.blit(self.background, (0, 0))
		pygame.display.update()

	def updateScreen(self):
		self.all.clear(self.screen, self.background)
		self.all.update()
		dirty=self.all.draw(self.screen)
		pygame.display.update(dirty)
