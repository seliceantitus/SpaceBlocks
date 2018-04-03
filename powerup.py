import pygame

import pygame
import sys

class Powerup(pygame.sprite.Sprite):

	pw_id = 0
	active_timestamp = 0
	speed_increase = 10
	speed_decrease = 5
	power_increase = 4

	def __init__(self, pw_id, width, height, pos_x, pos_y):
		pygame.sprite.Sprite.__init__(self)
		
		self.pw_id = pw_id
		
		if pw_id == 0:
			self.image = pygame.image.load("img/spwup.png")
		elif pw_id == 1:
			self.image = pygame.image.load("img/ppwup.png")
		elif pw_id == 2:
			self.image = pygame.image.load("img/bpwup.png")

		self.image = pygame.transform.scale(self.image, (width, height))
		self.image.set_colorkey((0, 0, 0))

		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self, increment_x, increment_y):
		self.rect.x += increment_x
		self.rect.y += increment_y

		if self.rect.y > 580:
			self.kill()

	def set_active(self, time):
		self.active_timestamp = time

	def get_active(self):
		return self.active_timestamp

	def get_id(self):
		return self.pw_id

	def get_speed_increase(self):
		return self.speed_increase

	def get_speed_decrease(self):
		return self.speed_decrease

	def get_power_increase(self):
		return self.power_increase