import pygame

class Player(pygame.sprite.Sprite):

	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("img/ship.png")
		self.image = pygame.transform.scale(self.image, (width, height))
		# self.image = pygame.Surface((width, height))
		# self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x = 10
		self.rect.y = 540
		
	def update(self, new_pos_x, new_pos_y):
		self.rect.x = new_pos_x
		self.rect.y = new_pos_y

	def get_x(self):
		return self.rect.x