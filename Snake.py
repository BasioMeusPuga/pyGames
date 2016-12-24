#!/usr/bin/python3

import sys
import random
import pygame
import os.path


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FPS = 60

pygame.init()
displaysurface = pygame.display.set_mode((400, 400))
displaysurface.fill(WHITE)
pygame.display.set_caption('Ghatiya snake')
clock = pygame.time.Clock()
my_dir = os.path.dirname(os.path.realpath(__file__))
food_sound = pygame.mixer.Sound(my_dir + '/resources/ping.wav')
oooh_sound = pygame.mixer.Sound(my_dir + '/resources/oooh.wav')


class GameState:
	score = 0
	speed_multiplier = 1
	paused = False
	game_over = False
	keylock = False


class Food:
	def __init__(self):
		self.foodx = 105
		self.foody = 105

	def new_food(self):
		self.foodx = random.randrange(15, 386, 10)
		self.foody = random.randrange(15, 386, 10)


class Snake:
	def __init__(self):
		self.segments = [[15, 5], [5, 5]]
		self.direction = 'RIGHT'

	def direction_update(self, direction_input):
		if self.direction == 'RIGHT' and direction_input == 'LEFT' or \
			self.direction == 'LEFT' and direction_input == 'RIGHT' or \
			self.direction == 'DOWN' and direction_input == 'UP' or \
			self.direction == 'UP' and direction_input == 'DOWN':
				pass
		else:
			if GameState.keylock is False:
				self.direction = direction_input
				GameState.keylock = True

	def embiggen(self):
		self.segments.append(self.segments[-1])


snek = Snake()
chow = Food()


def draw_me_like_one_of_your_french_girls():
	displaysurface.fill(WHITE)

	# Score
	font = pygame.font.SysFont('calibri', 20, bold=True)
	text = font.render(str(GameState.score), True, (0, 128, 0))
	x_c = len(str(GameState.score))
	text_rect = text.get_rect(center=(385 - x_c, 10))
	displaysurface.blit(text, text_rect)

	# Food
	pygame.draw.rect(displaysurface, GREEN, [chow.foodx, chow.foody, 10, 10])

	# Snake
	for i in snek.segments:
		pygame.draw.rect(displaysurface, BLACK, [i[0], i[1], 10, 10])


def snake_update():
	if snek.direction == 'UP':
		x_mult = 0
		y_mult = -1
	if snek.direction == 'DOWN':
		x_mult = 0
		y_mult = 1
	if snek.direction == 'LEFT':
		x_mult = -1
		y_mult = 0
	if snek.direction == 'RIGHT':
		x_mult = 1
		y_mult = 0

	new_snek = [[snek.segments[0][0] + (10 * x_mult), snek.segments[0][1] + (10 * y_mult)]]
	GameState.keylock = False
	for i in snek.segments[:-1]:
		new_snek.append(i)
	snek.segments = new_snek

	# Collisions
	snake_head = snek.segments[0]
	if snake_head in snek.segments[1:] or \
		(snake_head[0] < 5 or snake_head[0] > 395) or \
		(snake_head[1] < 5 or snake_head[1] > 395):
			oooh_sound.play()
			GameState.game_over = True

	def make_it_grow():
		snek.embiggen()
		chow.new_food()
		GameState.score += 1
		GameState.speed_multiplier = int(GameState.score / 5)
		food_sound.play()

	if snake_head == [chow.foodx, chow.foody]:
		make_it_grow()

	draw_me_like_one_of_your_french_girls()


def main():
	while True:
		if GameState.game_over is False:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						snek.direction_update('UP')
					elif event.key == pygame.K_DOWN:
						snek.direction_update('DOWN')
					elif event.key == pygame.K_LEFT:
						snek.direction_update('LEFT')
					elif event.key == pygame.K_RIGHT:
						snek.direction_update('RIGHT')
					elif event.key == pygame.K_RETURN:
						# Toggle Pause
						if GameState.paused is True:
							GameState.paused = False
						elif GameState.paused is False:
							GameState.paused = True
					elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
						pygame.quit()
						sys.exit()

				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if GameState.paused is False:
				snake_update()
				pygame.time.wait((100 - 10 * GameState.speed_multiplier))
			else:
				displaysurface.fill(WHITE)
				font = pygame.font.SysFont('calibri', 60, bold=True)
				text = font.render('PAUSED', True, RED)
				text_rect = text.get_rect(center=(200, 200))
				displaysurface.blit(text, text_rect)

		elif GameState.game_over is True:
			# Draw the head in red on getting a game over
			snake_head = snek.segments[0]
			pygame.draw.rect(displaysurface, RED, [snake_head[0], snake_head[1], 10, 10])

			# Game over message
			font = pygame.font.SysFont('calibri', 60, bold=True)
			text = font.render('GAME OVER', True, RED)
			text_rect = text.get_rect(center=(200, 200))
			displaysurface.blit(text, text_rect)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						# Reset all variables and restart the game on pressing r
						GameState.game_over = False
						GameState.score = 0
						GameState.speed_multiplier = 1
						snek.__init__()
						chow.__init__()
						main()
					elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
						pygame.quit()
						sys.exit()
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

		pygame.display.update()
		clock.tick(FPS)


if __name__ == '__main__':
	main()
