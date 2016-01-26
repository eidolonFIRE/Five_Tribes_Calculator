import pygame
import math
 
class Tile:
	def __init__():
		#               r,g,b,w,y
		self.meeples = [0,0,0,0,0]
		self.color = 'blue'             # or 'red'
		self.value = 0                  # victory point worth of the tile
		self.palmTrees = 0              # accumulated palm trees
		self.mosques = 0                # accumulated mosques
		self.camel = 'none'             # 'me', 'other'

class Player:
	def __init__():
		self.coin = 0                   # current savings
		self.camels = 9                 # camels remaining
		self.whiteMeeples = 0           # accumulated white meeples
		self.yellowsMeeples = 0         # accumulated yellow meeples

class Board:
	def __init__():
		self.tiles = [[Tile() for j in range(6)] for i in range(5)]

pygame.init()


testRect = baseDraw((50,50))

gameDisplay = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Five Tribes Calculator')

gameExit = False

clock = pygame.time.Clock()
while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				gameExit = True
 
	gameDisplay.fill(white)
	testRect.update()
	testRect.draw()
	pygame.display.update()
	clock.tick(60)
 
pygame.quit()
quit()