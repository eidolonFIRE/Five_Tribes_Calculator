import pygame
import math
import random

# NOTES ON MEEPLE PLACEMENT

# 1
#    - 1 -
#    1 X 1
#    - 1 -

# 2
#    - - 1 - -
#    - 1 - 1 -
#    1 - X - 1
#    - 1 - 1 -
#    - - 1 - -

# 3
#    - - - 1 - - -
#    - - 1 - 1 - -
#    - 1 - 1 - 1 -
#    1 - 1 X 1 - 1
#    - 1 - 1 - 1 -
#    - - 1 - 1 - -
#    - - - 1 - - -

# 4
#    - - - - 1 - - - -
#    - - - 1 - 1 - - -
#    - - 1 - 1 - 1 - -
#    - 1 - 1 - 1 - 1 -
#    1 - 1 - 1 - 1 - 1
#    - 1 - 1 - 1 - 1 -
#    - - 1 - 1 - 1 - -
#    - - - 1 - 1 - - -
#    - - - - 1 - - - -

# 5
#    - - - - - 1 - - - - -
#    - - - - 1 - 1 - - - -
#    - - - 1 - 1 - 1 - - -
#    - - 1 - 1 - 1 - 1 - -
#    - 1 - 1 - 2 - 1 - 1 -
#    1 - 1 - 2 X 2 - 1 - 1
#    - 1 - 1 - 2 - 1 - 1 -
#    - - 1 - 1 - 1 - 1 - -
#    - - - 1 - 1 - 1 - - -
#    - - - - 1 - 1 - - - -
#    - - - - - 1 - - - - -

# 6
#    - - - - - - 1 - - - - - -
#    - - - - - 1 - 1 - - - - -
#    - - - - 1 - 1 - 1 - - - -
#    - - - 1 - 1 - 1 - 1 - - -
#    - - 1 - 1 - 2 - 1 - 1 - -
#    - 1 - 1 - 1 - 2 - 1 - 1 -
#    1 - 1 - 2 - 1 - 2 - 1 - 1
#    - 1 - 1 - 2 - 2 - 1 - 1 -
#    - - 1 - 1 - 2 - 1 - 1 - -
#    - - - 1 - 1 - 1 - 1 - - -
#    - - - - 1 - 1 - 1 - - - -
#    - - - - - 1 - 1 - - - - -
#    - - - - - - 1 - - - - - -





availableTiles = \
	[('blue', 5 , 'village')] * 5 + \
	[('blue', 6 , 'djinn')  ] * 4 + \
	[('blue', 10, 'djinn'),         \
	 ('blue', 12, 'djinn'),         \
	 ('blue', 15, 'djinn')  ] +     \
	[('red', 4, 'l_market') ] * 4 + \
	[('red', 6, 's_market') ] * 8 + \
	[('red', 8, 'palm')     ] * 6


class Tile:
	meepleColor = [
					(240,  0,  0),  
					(0  ,230,  0),  
					(0  ,  0,250),  
					(250,250,250),
					(240,240,  0),  ]
	size = 100

	def __init__(self, setup):
		#               r,g,b,w,y
		#self.meeples = [random.randrange(2),random.randrange(2),random.randrange(2),random.randrange(2),random.randrange(2)]
		self.meeples = [2,0,0,0,0]
		self.color = setup[0]        
		self.value = setup[1]                  # victory point worth of the tile
		self.reward = setup[2]
		self.palmTrees = 0                     # accumulated palm trees
		self.village = 0                       # accumulated village
		self.camel = 'none'                    # 'me', 'other'


	def draw(self, x, y):
		# background
		pygame.draw.rect(gameDisplay, (200, 200, 200), [x,y,Tile.size,Tile.size])
		if self.color == 'blue':
			pygame.draw.circle(gameDisplay, (150,150,240), [x + Tile.size * 9/10, y + Tile.size * 1/10], Tile.size / 10)
		if self.color == 'red':
			pygame.draw.circle(gameDisplay, (240,150,150), [x + Tile.size * 9/10, y + Tile.size * 1/10], Tile.size / 10)
			# draw tile value text
		font = pygame.font.Font(None, Tile.size * 1/5)
		text = font.render(str(self.value), 1, (10,10,10))
		textpos = (
			-text.get_rect().center[0] + x + Tile.size * 9/10, 
			-text.get_rect().center[1] + y + Tile.size * 1/10)
		gameDisplay.blit(text, textpos)

		# board color and value

		# meeples
		cX = Tile.size * 1/4
		cY = Tile.size * 1/4
		for meep in range(5):
			for stack in range(self.meeples[meep]):
				pygame.draw.circle(gameDisplay, Tile.meepleColor[meep],   [x + cX, y + cY], Tile.size / 8)
				cX += Tile.size * 1/4
				if cX >= Tile.size:
					cX = Tile.size * 1/4
					cY += Tile.size * 1/4
					if cY >= Tile.size:
						cX = Tile.size * 3/8
						cY = Tile.size * 3/8


class Player:
	def __init__(self):
		self.coin = 0                   # current savings
		self.camels = 9                 # camels remaining
		self.whiteMeeples = 0           # accumulated white meeples
		self.yellowsMeeples = 0         # accumulated yellow meeples

def getTile():
	myPool = availableTiles
	retval = myPool[0]
	myPool.remove(retval)
	return retval


class Board:
	width = 6
	height = 5
	tileSpacing = 10
	def __init__(self):
		self.tiles = [[Tile(setup = getTile()) for j in range(Board.height)] for i in range(Board.width)]
	def draw(self):
		for x in range(Board.width):
			for y in range(Board.height):
				self.tiles[x][y].draw(x = x * (Tile.size + Board.tileSpacing), y = y * (Tile.size + Board.tileSpacing))
	def clickTile(self, x, y):
		retval = 0
		tileX = x / (Tile.size + self.tileSpacing)
		tileY = y / (Tile.size + self.tileSpacing)

		#print tileX, tileY

		# if selection is within bounds
		if tileX >= 0 and tileX < Board.width and tileY >= 0 and tileY < Board.height:
			retval = getResolvableTiles(tileX, tileY, Board.width, Board.height, radius= sum(self.tiles[tileX][tileY].meeples) + 1)
		return retval


#==============================================================================



def getResolvableTiles(x = 0, y = 0, w = 0, h = 0, radius = 0):
	xy_pairs = []
	
	for scanx in range(0, radius):
		for scany in range(0, radius):
			if scanx == 0 and scany == 0:
				continue
			if (scanx + scany) % 2 == 0 and (scanx + scany) <= radius:
				xy_pairs = xy_pairs + [(x + scanx, y + scany)]
				if scanx != 0:
					xy_pairs = xy_pairs + [(x - scanx, y + scany)]
				if scany != 0:
					xy_pairs = xy_pairs + [(x + scanx, y - scany)]
				if scanx != 0 and scany !=0:
					xy_pairs = xy_pairs + [(x - scanx, y - scany)]
	if radius % 2 == 0 and radius > 2:
		xy_pairs = xy_pairs + [(x, y)]

	# clean up pairs
	for pair in xy_pairs:
		if pair[0] < 0 or pair[0] >= w \
		or pair[1] < 0 or pair[1] >= h:
			xy_pairs.remove(pair)
	return xy_pairs




def resolveTile(tile):
	return







#==============================================================================


pygame.init()

myBoard = Board()

gameDisplay = pygame.display.set_mode((700,700))
pygame.display.set_caption('Five Tribes Calculator')

gameExit = False

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				gameExit = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()

			print myBoard.clickTile(x = pos[0],y = pos[1])
 
	gameDisplay.fill((0,0,0))
	myBoard.draw()
	pygame.display.update()
 
pygame.quit()
quit()