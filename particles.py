import pygame

class Particle(pygame.sprite.Sprite):

	def __init__(self, x, y, dx, dy, size, color):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((size, size))
		self.image.fill(color)
		self.rect = self.image.get_rect()

		self.x_velocity = dx
		self.y_velocity = dy
		self.rect.x = x
		self.rect.y = y

		self.gravity = 0.25

	def update(self):
		self.y_velocity += self.gravity / 2
		self.rect.x += self.x_velocity
		self.rect.y += self.y_velocity

		if self.check_bounds():
			self.kill()

	def check_bounds(self):
		if self.rect.x <= 0 or self.rect.x >= 401:
			return True
		elif self.rect.y <= 0 or self.rect.y >= 701:
			return True
		else:
			return False