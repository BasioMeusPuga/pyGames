#!/usr/bin/python3

import pygame
import pygame.gfxdraw
import os.path
from math import sqrt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60

DISPLAYWIDTH = 300
DISPLAYHEIGHT = 300

pygame.init()
displaysurface = pygame.display.set_mode((DISPLAYHEIGHT, DISPLAYWIDTH))
displaysurface.fill(WHITE)
pygame.display.set_caption('Ghatiya TicTacToe')
clock = pygame.time.Clock()
my_dir = os.path.dirname(os.path.realpath(__file__))
click_sound = pygame.mixer.Sound(my_dir + '/resources/ping.wav')
yay_sound = pygame.mixer.Sound(my_dir + '/resources/yay.wav')


class GameState:
	game_over = False
	victor = None


class GameGrid:
	"""
	0	|	1	|	2
	-----------------
	3	|	4	|	5
	-----------------
	6	|	7	|	8
	"""

	def __init__(self):
		self.turn = 0
		self.rectangles = []
		self.status = [None for i in range(9)]
		displaysurface.fill(WHITE)

		# Draw the invisible rectangles that make up the grid
		rectangle = 0
		for i in range(3):
			for j in range(3):
				self.rectangles.append([rectangle, pygame.draw.rect(displaysurface, WHITE, [30 + j * 80, 30 + i * 80, 80, 80])])
				rectangle += 1

		# Draw the Grid
		pygame.draw.line(displaysurface, BLACK, (110, 30), (110, 270), 3)
		pygame.draw.line(displaysurface, BLACK, (190, 30), (190, 270), 3)
		pygame.draw.line(displaysurface, BLACK, (30, 110), (270, 110), 3)
		pygame.draw.line(displaysurface, BLACK, (30, 190), (270, 190), 3)

	def place_symbol(self, mouse_coordinates):
		for i in self.rectangles:
			rectangle_object = i[1]
			if rectangle_object.collidepoint(mouse_coordinates):
				clicked_rectangle = i[0]
				break

		try:
			if self.status[clicked_rectangle] is None:
				self.status[clicked_rectangle] = self.turn
				self.squigglies(self.status[clicked_rectangle], rectangle_object.center)

				if self.turn == 0:
					self.turn = 1
				elif self.turn == 1:
					self.turn = 0

				self.evaluate()
		except UnboundLocalError:
			pass

	def squigglies(self, symbol, grid_coordinates):
		grid_x = grid_coordinates[0]
		grid_y = grid_coordinates[1]

		if symbol == 0:
			pygame.gfxdraw.aacircle(displaysurface, grid_x, grid_y, 30, BLUE)
		elif symbol == 1:
			diagonal = 30 // sqrt(2)

			pygame.draw.line(
				displaysurface, GREEN,
				(grid_x - diagonal, grid_y - diagonal),
				(grid_x + diagonal, grid_y + diagonal),
				3)
			pygame.draw.line(
				displaysurface, GREEN,
				(grid_x - diagonal, grid_y + diagonal),
				(grid_x + diagonal, grid_y - diagonal),
				3)

	def evaluate(self):
		win_conditions = [
			[0, 1, 2],
			[0, 3, 6],
			[0, 4, 8],
			[1, 4, 7],
			[2, 4, 6],
			[2, 5, 8],
			[3, 4, 5],
			[6, 7, 8]
		]

		for i in win_conditions:
			if self.status[i[0]] == self.status[i[1]] == self.status[i[2]] and (self.status[i[0]] is not None):
				yay_sound.play()
				if self.turn == 0:
					GameState.victor = 'CROSSES'
				elif self.turn == 1:
					GameState.victor = 'CIRCLES'
				GameState.game_over = True
			else:
				click_sound.play()

		squares_remaining = self.status.count(None)
		if squares_remaining == 0:
			GameState.game_over = True


def main():
	grid = GameGrid()
	while True:
		if GameState.game_over is False:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						exit()
					if event.key == pygame.K_r:
						main()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					grid.place_symbol(pygame.mouse.get_pos())

				elif event.type == pygame.QUIT:
					pygame.quit()
					exit()

		elif GameState.game_over is True:
			if GameState.victor is None:
				displaytext = 'DRAW!'
			else:
				displaytext = GameState.victor + ' WIN!'

			font = pygame.font.SysFont('calibri', 40, bold=True)
			text = font.render(displaytext, True, RED)
			text_rect = text.get_rect(center=(150, 150))
			displaysurface.blit(text, text_rect)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						exit()
					elif event.key == pygame.K_r:
						GameState.victor = None
						GameState.game_over = False
						main()

				elif event.type == pygame.QUIT:
					pygame.quit()
					exit()

		pygame.display.update()
		clock.tick(FPS)


if __name__ == '__main__':
	main()
