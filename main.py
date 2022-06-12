#!/usr/bin/env python2

import pygame
import random
import pygame.math

WIDTH = 1280
HEIGHT = 720
FPS_MAX = 60

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


## initialize pygame and create window
pygame.init()
pygame.font.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()  ## For syncing the FPS
display = pygame.Surface((WIDTH / 2, HEIGHT / 2)) # initiate a display to paste all images to, that is half of desired size, will scale up later so all sprites are bigger
## group all the sprites together for ease of update
player_image = pygame.image.load('dave.png')

#camera

# initialize debugger

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Debug:
	def __init__(self):
		self.debug_list = []

	def add_debug(self, name, value):
		self.debug_list.append([name, value])

	def draw(self):
		self.font = pygame.font.SysFont('Comic Sans MS', 10)
		spacing = 0
		for debug_item in self.debug_list:
			text_surface = self.font.render("{0}: {1}".format(debug_item[0], debug_item[1]), False, (255, 0, 0))

			display.blit(text_surface, (0, 0 * spacing))
			spacing += 1


class Player:

	def __init__(self, x, y, width, height):
		self.position = pygame.math.Vector2(0, 0)
		self.width = width
		self.height = height
		self.move_speed = 10
		self.moving_directions = {'up': False,
		                          'down': False,
		                          'left': False,
		                          'right': False}

		self.move_vector = pygame.Vector2(0, 0)


#               posx, posy,width,height
player = Player(10, 10, 16, 32)

# camera
true_camera_offset = Position(0,0)
CAMERA_SPEED = 20
# movement

## Game loop
running = True
while running:
	FPS = clock.get_fps()
	pygame.display.set_caption("Dave In A Cave  _FPS{0}".format(FPS))
	# 1 Process input/events
	 ## will make the loop run at the same speed all the time
	dt = clock.tick() / 1000
	for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
		## listening for the the X button at the top
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				player.moving_directions['left'] = True
			if event.key == pygame.K_d:
				player.moving_directions['right'] = True
			if event.key == pygame.K_w:
				player.moving_directions['up'] = True
			if event.key == pygame.K_s:
				player.moving_directions['down'] = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				player.moving_directions['left'] = False
			if event.key == pygame.K_d:
				player.moving_directions['right'] = False
			if event.key == pygame.K_w:
				player.moving_directions['up'] = False
			if event.key == pygame.K_s:
				player.moving_directions['down'] = False

	# update move vector
	if player.moving_directions['left'] or player.moving_directions['right']:
		if player.moving_directions['left']:
			player.move_vector.x = -1
		if player.moving_directions['right']:
			player.move_vector.x = 1
	else :
		player.move_vector.x = 0
	if player.moving_directions['up'] or player.moving_directions['down']:
		if player.moving_directions['up']:
			player.move_vector.y = -1
		if player.moving_directions['down']:
			player.move_vector.y = 1
	else :
		player.move_vector.y = 0
	# normalize player move vector so it does not move faster diagnally
	if player.move_vector.length() >1:
		pygame.math.Vector2.scale_to_length(player.move_vector,1.0)


	# move vector by delta time for universal movement on different computer speeds
	# How the camera works:
		# Player position moves in the world space
		# move ALL sprites (map sprites/enemy sprites/ player sprite) to a position that sets player at the CENTER of the screen
	# move player
	player.position.x += player.move_vector.x
	player.position.y += player.move_vector.y

	# get offset that we need to offset all sprites off to set player at center
	true_camera_offset.x += (player.position.x - true_camera_offset.x - display.get_width()/4 + (player_image.get_width() / 2) ) / CAMERA_SPEED
	true_camera_offset.y += (player.position.y - true_camera_offset.y - display.get_height() / 4 + (player_image.get_height() / 2) ) / CAMERA_SPEED

	# convert offset to INT so it doesnt move as fractionally
	camera_offset = Position(true_camera_offset.x, true_camera_offset.y)
	camera_offset.x = int(true_camera_offset.x)
	camera_offset.y = int(true_camera_offset.y)
	# add move vector to player camera offset




	# 2 Update


	# 3 Draw/render
	display.fill((200, 200, 200))

	for row in range(100):
		pygame.draw.line(display, (0,0,0), [0 - camera_offset.x, row * 10- camera_offset.y], [1000- camera_offset.x,row * 10- camera_offset.y])
	for col in range(100):
		pygame.draw.line(display, (0,0,0), [col * 10- camera_offset.x, 0- camera_offset.y], [col * 10- camera_offset.x, 1000- camera_offset.y])

	########################
	# drawing player to display
	display.blit(player_image, [player.position.x - camera_offset.x, player.position.y - camera_offset.y])

	pygame.draw.rect(display,(255, 0,0), pygame.Rect(0 - camera_offset.x, 10 - camera_offset.y, 10, 10))
	# scaling display to width, height of screen
	surf = pygame.transform.scale(display, (WIDTH * 2 , HEIGHT * 2))
	# drawing display
	screen.blit(surf, (0,0))
	### Your code comes here

	########################


	## Done after drawing everything to the screen
	pygame.display.flip()
	clock.tick(60)
pygame.quit()