#!/usr/bin/python3

import time
import pygame
import random

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
	gravity = 2700  # Increased gravity and shorter jump time > more displacement
	groundlevel = DISPLAYHEIGHT - 100
	initial_speed = 4


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
		self.image = pygame.image.load('resources/supes_small.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)  # The image mask allows for better collision handling

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
		self.image = pygame.image.load('resources/kryptonite_small.png').convert_alpha()
		self.offset = offset
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

		# Put the sprite @ ground level
		self.rect.x = 800 - self.offset
		self.rect.y = Options.groundlevel - 25

	def update(self):
		speed_multiplier = GameState.score // 500
		GameState.speed = Options.initial_speed + .5 * speed_multiplier
		self.rect.x += -1 * GameState.speed
		if self.rect.center[0] < 0:  # Remove the sprite when the x coordinate of the center crosses the left screen edge
			self.kill()


def lex_luthor():
	time_delta = time.time() - GameState.last_tree_gen
	if time_delta * GameState.speed < 15:
		return

	number_of_crystals = random.randrange(2, 5)

	offset = 0
	for i in range(number_of_crystals):
		new_crystal = Tree(offset)
		all_sprites_list.add(new_crystal)
		obstacles.add(new_crystal)
		offset += 15

	GameState.last_tree_gen = time.time()


def collisions():
	for i in obstacles:
		collision_list = pygame.sprite.collide_mask(superdude, i)
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
		text_rect = text.get_rect(center=(740 - x_c, 10))
		displaysurface.blit(text, text_rect)


def main():
	# Initialize first "tree" and the "runner"
	# I'm using global variables because it makes resetting the game easier
	global superdude, kryptonite, all_sprites_list, obstacles

	superdude = Runner()
	kryptonite = Tree(5)

	all_sprites_list = pygame.sprite.Group()
	obstacles = pygame.sprite.Group()

	all_sprites_list.add(superdude)
	all_sprites_list.add(kryptonite)
	obstacles.add(kryptonite)

	while True:
		if GameState.game_over is False:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:

						if GameState.keylock is False:
							GameState.keylock = True
							GameState.jump_start_time = time.time()

					if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
						pygame.quit()
						exit()
					if event.key == pygame.K_r:
						main()

				elif event.type == pygame.QUIT:
					pygame.quit()
					exit()

			displaysurface.fill(WHITE)  # This is needed because otherwise the update method leaves a trail
			lex_luthor()
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
						main()

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
	main()
