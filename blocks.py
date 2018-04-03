import pygame
import sys

class Block(pygame.sprite.Sprite):
	pygame.font.init()
	font = pygame.font.SysFont('Calibri', 30, True, False)
	font_color = pygame.Color('white')
	
	value = 0
	color = ()

	def __init__(self, color, width, height, pos_x, pos_y, value):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.image.set_colorkey((0, 0, 0))

		self.value = value
		self.color = color

		text_surface = self.font.render(str(value), True, self.font_color)
		text_rect = text_surface.get_rect(center = self.image.get_rect().center)

		self.image.blit(text_surface, text_rect)

		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y

	def update_text(self):
		self.image.fill(self.color)

		text_surface = self.font.render(str(self.value), True, self.font_color)
		text_rect = text_surface.get_rect(center = self.image.get_rect().center)

		self.image.blit(text_surface, text_rect)

	def scale_out(self):	
		(w, h) = (self.image.get_rect().x, self.image.get_rect().y)
		w -= 5
		h -= 5
		if w <= 0 or h <= 0:
			self.kill()
		else:
			self.image = pygame.transform.scale(self.image, (w, h))

	def update(self, increment_x, increment_y):
		self.rect.x += increment_x
		self.rect.y += increment_y

		self.update_text()

		if self.rect.y > 566:
			self.scale_out()

	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = value

	def get_x(self):
		return self.rect.x

	def get_y(self):
		return self.rect.y

	def get_color(self):
		return self.color
