#!/usr/bin/python3

import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60

DISPLAYWIDTH = 800
DISPLAYHEIGHT = 300

pygame.init()
displaysurface = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
displaysurface.convert_alpha()
displaysurface.fill(WHITE)
pygame.display.set_caption('Ghatiya Runner')
clock = pygame.time.Clock()


class Options:
	jump_time = .25  # Either side of the jump. Total jump time = jump_time * 2
	gravity = 2000  # Increased gravity and shorter jump time > more displacement
	groundlevel = DISPLAYHEIGHT - 100
	initial_speed = 3


class GameState:
	game_over = False
	pause = False
	score = 0
	highscore = 0
	speed = Options.initial_speed

	keylock = False
	jump_start_time = None

	last_tree_gen = time.time()


class Runner(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		width = 20
		height = 30
		self.image = pygame.image.load('resources/supes_small.png').convert_alpha()
		self.rect = self.image.get_rect()

		# Put the sprite @ ground level
		self.rect.x = 20
		self.rect.y = Options.groundlevel - 55

	def update(self):
		if GameState.jump_start_time is not None:
			self.current_pos()

	def current_pos(self):
		# I'm sorry, Newton
		initial_velocity = Options.jump_time * Options.gravity
		apogee = (initial_velocity ** 2) / (2 * Options.gravity)

		time_delta = time.time() - GameState.jump_start_time

		if time_delta <= Options.jump_time:
			displacement = initial_velocity * time_delta - .5 * Options.gravity * (time_delta ** 2)
			self.rect.y = Options.groundlevel - 55 - round(displacement)

		elif Options.jump_time < time_delta < Options.jump_time * 2:
			displacement = .5 * Options.gravity * ((time_delta - Options.jump_time) ** 2)
			self.rect.y = Options.groundlevel - 55 - round(apogee - displacement)

		else:
			GameState.keylock = False
			self.rect.y = Options.groundlevel - 55


class Tree(pygame.sprite.Sprite):
	def __init__(self, offset):
		pygame.sprite.Sprite.__init__(self)
		width = 5
		height = 35
		self.image = pygame.Surface([width, height])
		self.image.fill(BLACK)
		self.offset = offset
		self.rect = self.image.get_rect()

		# Put the sprite @ ground level
		self.rect.x = 800 - self.offset
		self.rect.y = Options.groundlevel - 5

	def update(self):
		speed_multiplier = GameState.score // 500
		GameState.speed = Options.initial_speed + .5 * speed_multiplier
		self.rect.x += -1 * GameState.speed
		if self.rect.x < 0:
			self.kill()


def farmer():
	time_delta = time.time() - GameState.last_tree_gen
	if time_delta * GameState.speed < 15:
		return

	number_of_trees = random.randrange(2, 5)

	offset = 0
	for i in range(number_of_trees):
		new_tree = Tree(offset)
		all_sprites_list.add(new_tree)
		obstacles.add(new_tree)
		offset += 10

	GameState.last_tree_gen = time.time()


def collisions():
	collision_list = pygame.sprite.spritecollide(stickdude, obstacles, False)
	if collision_list:
		GameState.game_over = True


def score():
	score_multiplier = GameState.score // 500
	GameState.score += .5 + .5 * score_multiplier
	display_score = int(GameState.score)

	# Display score
	font = pygame.font.SysFont('calibri', 20, bold=True)
	text = font.render(str(display_score), True, (0, 128, 0))
	x_c = len(str(display_score))
	text_rect = text.get_rect(center=(780 - x_c, 10))
	displaysurface.blit(text, text_rect)

	# Display high score
	if GameState.highscore != 0:
		font = pygame.font.SysFont('calibri', 20, bold=True)
		text = font.render(str(int(GameState.highscore)), True, BLUE)
		x_c = len(str(GameState.highscore))
		text_rect = text.get_rect(center=(750 - x_c, 10))
		displaysurface.blit(text, text_rect)


def start():
	# Initialize first "tree" and the "runner"
	global stickdude, shitty_tree, all_sprites_list, obstacles

	stickdude = Runner()
	shitty_tree = Tree(5)

	all_sprites_list = pygame.sprite.Group()
	obstacles = pygame.sprite.Group()

	all_sprites_list.add(stickdude)
	all_sprites_list.add(shitty_tree)
	obstacles.add(shitty_tree)

	main()


def main():
	while True:
		if GameState.game_over is False:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:

						if GameState.keylock is False:
							GameState.keylock = True
							GameState.jump_start_time = time.time()

					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						exit()
					if event.key == pygame.K_r:
						main()

				elif event.type == pygame.QUIT:
					pygame.quit()
					exit()

			displaysurface.fill(WHITE)  # This is needed because otherwise the update method leaves a trail
			farmer()
			all_sprites_list.update()
			score()
			collisions()
			all_sprites_list.draw(displaysurface)

		elif GameState.game_over is True:
			# Game over message
			font = pygame.font.SysFont('calibri', 60, bold=True)
			text = font.render('GAME OVER', True, RED)
			text_rect = text.get_rect(center=(DISPLAYWIDTH // 2, DISPLAYHEIGHT // 2))
			displaysurface.blit(text, text_rect)

			if GameState.score > GameState.highscore:
				GameState.highscore = GameState.score

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r or event.key == pygame.K_RETURN:
						GameState.game_over = False
						GameState.score = 0
						start()

					if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
						pygame.quit()
						exit()

				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

		pygame.draw.line(displaysurface, BLACK, (0, Options.groundlevel + 32), (800, Options.groundlevel + 32), 3)
		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	start()
