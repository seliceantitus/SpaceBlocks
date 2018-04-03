import pygame

class Bullet(pygame.sprite.Sprite):
	boost = 0
	angle = 0

	def __init__(self, boost, width, height, pos_x, pos_y, rotate_angle):
		pygame.sprite.Sprite.__init__(self)
		
		self.boost = boost
		self.angle = rotate_angle
		
		if boost == -1:
			self.image = pygame.image.load("img/bullet.png")
		elif boost == 0:
			self.image = pygame.image.load("img/bullet_s.png")
		elif boost == 1:
			self.image = pygame.image.load("img/bullet_p.png")
		elif boost == 2:
			self.image = pygame.image.load("img/bullet_b.png")
			self.image = pygame.transform.rotate(self.image, rotate_angle)
		self.image = pygame.transform.scale(self.image, (width, height))

		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y
		
	def update(self, incremet_x, increment_y):
		if self.boost == 2:
			if self.angle < 0:
				self.rect.x += 1
			elif self.angle > 0:
				self.rect.x -= 1

		self.rect.x -= incremet_x
		self.rect.y -= increment_y

		if self.rect.y <= 0 or self.rect.x > 401 or self.rect.x < 0:
			self.kill()