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
point = pygame.mixer.Sound('resources/laser_point.wav')


class Options:
	initial_speed = 2.5


class GameState:
	pause = False
	player1_score = 0
	player2_score = 0
	collisions = 0
	speed = Options.initial_speed
	countdown = 3


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
		GameState.countdown = 3
		self.image = pygame.image.load('resources/DeathStar_small.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

		self.rect.x = DISPLAYWIDTH // 2 - 10
		self.rect.y = DISPLAYHEIGHT // 2 - 10

		self.x_speed = random.choice([1, -1])
		self.y_speed = random.choice([1, -1])

		GameState.speed = Options.initial_speed
		GameState.collisions = 0

	def update(self):
		# Check for collision with the upper/lower wall
		if self.rect.y <= 0 or self.rect.y >= DISPLAYHEIGHT - 15:
			self.y_speed *= -1

		# Check for collision with the left/right wall
		if self.rect.x <= 0:
			GameState.player2_score += 1
			point.play()
			self.__init__()
		elif self.rect.x >= DISPLAYWIDTH - 15:
			GameState.player1_score += 1
			point.play()
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

		if GameState.countdown == -1:
			self.rect.x += self.x_speed * round(GameState.speed)
			self.rect.y += self.y_speed * round(GameState.speed)

	def collision_common(self):
		self.x_speed *= -1
		GameState.collisions += 1
		lightsaber.play()

		# Increase speed by .5 for every 3 collisions
		speed_increase = (GameState.collisions // 3 + 1) / 2
		GameState.speed = Options.initial_speed + 1 * speed_increase


def make_text(displaytext, size, x_center, y_center, color):
	font = pygame.font.SysFont('calibri', size, bold=False)
	text = font.render(str(displaytext), True, color)
	x_c = len(str(displaytext))
	text_rect = text.get_rect(center=(x_center - x_c, y_center))
	displaysurface.blit(text, text_rect)


def score():
	make_text(GameState.player1_score, 20, 285, 10, WHITE)
	make_text(GameState.player2_score, 20, 315, 10, WHITE)


def first_run():
	make_text(GameState.countdown, 80, 300, DISPLAYHEIGHT - 40, WHITE)
	GameState.countdown -= 1
	pygame.time.wait(800)


def main():
	global player1, player2, ball, sprites
	player1 = Paddle(1)
	player2 = Paddle(2)
	ball = Ball()

	sprites = pygame.sprite.Group()
	sprites.add(player1, player2, ball)

	while True:
		if GameState.countdown == -1:
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

		displaysurface.fill(BLACK)
		if GameState.countdown > -1:
			first_run()

		sprites.update()
		score()
		sprites.draw(displaysurface)
		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()
