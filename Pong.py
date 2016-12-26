#!/usr/bin/python3

import pygame
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60

DISPLAYWIDTH = 600
DISPLAYHEIGHT = 400

pygame.init()
displaysurface = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
displaysurface.convert_alpha()
pygame.display.set_caption('Ghatiya Pong')
clock = pygame.time.Clock()
lightsaber = pygame.mixer.Sound('resources/lightsaber.wav')


class Options:
	initial_speed = 1.5


class GameState:
	pause = False
	player1_score = 0
	player2_score = 0
	collisions = 0
	speed = Options.initial_speed


class Paddle(pygame.sprite.Sprite):
	def __init__(self, player):
		pygame.sprite.Sprite.__init__(self)
		self.player = player
		self.image = pygame.image.load('resources/LightSaber_small.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

		if self.player == 1:
			self.rect.x = 10
		elif self.player == 2:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.x = DISPLAYWIDTH - 15

		self.rect.y = DISPLAYHEIGHT // 2 - 30

	def move(self, direction):
		if direction == 'UP' and self.rect.y >= 20:
			self.rect.y += -10
		elif direction == 'DOWN' and self.rect.y <= DISPLAYHEIGHT - 80:
			self.rect.y += 10


class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('resources/DeathStar_small.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

		self.rect.x = DISPLAYWIDTH // 2 - 10
		self.rect.y = DISPLAYHEIGHT // 2 - 10

		self.x_speed = random.choice([1, -1])
		self.y_speed = random.choice([1, -1])

	def update(self):
		displaysurface.fill(BLACK)

		# Check for collision with the upper/lower wall
		if self.rect.y <= 0 or self.rect.y >= DISPLAYHEIGHT - 15:
			self.y_speed *= -1

		# Check for collision with the left/right wall
		if self.rect.x <= 0:
			GameState.player2_score += 1
			self.__init__()
		elif self.rect.x >= DISPLAYWIDTH - 15:
			GameState.player1_score += 1
			self.__init__()

		# Check for collisions with either of the paddles
		collision_left = pygame.sprite.collide_mask(ball, player1)
		if collision_left:
			self.collision_common()
			self.rect.x = 15

		collision_right = pygame.sprite.collide_mask(ball, player2)
		if collision_right:
			self.collision_common()
			self.rect.x = DISPLAYWIDTH - 31

		self.rect.x += self.x_speed * round(GameState.speed)
		self.rect.y += self.y_speed * round(GameState.speed)

	def collision_common(self):
		self.x_speed *= -1
		GameState.collisions += 1
		lightsaber.play()

		# speed_increase = (GameState.collisions // 1 + 1) // 2
		# GameState.speed = Options.initial_speed + 1 * speed_increase


def score():
	pass


def main():
	global player1, player2, ball, sprites
	player1 = Paddle(1)
	player2 = Paddle(2)
	ball = Ball()

	sprites = pygame.sprite.Group()
	sprites.add(player1, player2, ball)

	while True:
		key_held = pygame.key.get_pressed()

		if key_held[pygame.K_w]:
			player1.move('UP')
		if key_held[pygame.K_s]:
			player1.move('DOWN')

		if key_held[pygame.K_UP]:
			player2.move('UP')
		if key_held[pygame.K_DOWN]:
			player2.move('DOWN')

		for event in pygame.event.get():

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					pygame.quit()
					exit()
				if event.key == pygame.K_r:
					main()

			elif event.type == pygame.QUIT:
				pygame.quit()
				exit()

		sprites.update()
		sprites.draw(displaysurface)
		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()
