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
#    - 1 - 1 - 1 - 1 - 1 -
#    1 - 1 - 1 X 1 - 1 - 1
#    - 1 - 1 - 1 - 1 - 1 -
#    - - 1 - 1 - 1 - 1 - -
#    - - - 1 - 1 - 1 - - -
#    - - - - 1 - 1 - - - -
#    - - - - - 1 - - - - -

# 6
#    - - - - - - 1 - - - - - -
#    - - - - - 1 - 1 - - - - -
#    - - - - 1 - 1 - 1 - - - -
#    - - - 1 - 1 - 1 - 1 - - -
#    - - 1 - 1 - 1 - 1 - 1 - -
#    - 1 - 1 - 1 - 1 - 1 - 1 -
#    1 - 1 - 1 - 1 - 1 - 1 - 1
#    - 1 - 1 - 1 - 1 - 1 - 1 -
#    - - 1 - 1 - 1 - 1 - 1 - -
#    - - - 1 - 1 - 1 - 1 - - -
#    - - - - 1 - 1 - 1 - - - -
#    - - - - - 1 - 1 - - - - -
#    - - - - - - 1 - - - - - -








class Tile:
	availableTiles_counter = 1
	availableTiles = \
	[('blue', 5 , 'village')] * 5 + \
	[('blue', 6 , 'djinn')  ] * 4 + \
	[('blue', 10, 'djinn'),
	 ('blue', 12, 'djinn'),
	 ('blue', 15, 'djinn')  ] + \
	[('red', 4, 'l_market') ] * 4 + \
	[('red', 6, 's_market') ] * 8 + \
	[('red', 8, 'palm')     ] * 6


	meepleColor = [
					(240,  0,  0),  
					(0  ,230,  0),  
					(0  ,  0,250),  
					(250,250,250),
					(240,240,  0),  ]

	def __init__(self, pool, size = 100):
		#               r,g,b,w,y
		setup = pool[Tile.availableTiles_counter]
		self.meeples = [random.randrange(2),random.randrange(2),random.randrange(2),random.randrange(2),random.randrange(2)]
		self.color = setup[0]        
		self.value = setup[1]                  # victory point worth of the tile
		self.reward = setup[2]
		self.palmTrees = 0                     # accumulated palm trees
		self.village = 0                       # accumulated village
		self.camel = 'none'                    # 'me', 'other'
		self.size = size                       # render size

		Tile.availableTiles_counter = Tile.availableTiles_counter + 1

	def draw(self, x, y):
		# background
		pygame.draw.rect(gameDisplay, (200, 200, 200), [x,y,self.size,self.size])
		if self.color == 'blue':
			pygame.draw.circle(gameDisplay, (150,150,240), [x + self.size * 9/10, y + self.size * 1/10], self.size / 10)
		if self.color == 'red':
			pygame.draw.circle(gameDisplay, (240,150,150), [x + self.size * 9/10, y + self.size * 1/10], self.size / 10)
			# draw tile value text
		font = pygame.font.Font(None, self.size * 1/5)
		text = font.render(str(self.value), 1, (10,10,10))
		textpos = (
			-text.get_rect().center[0] + x + self.size * 9/10, 
			-text.get_rect().center[1] + y + self.size * 1/10)
		gameDisplay.blit(text, textpos)

		# board color and value

		# meeples
		cX = self.size * 1/4
		cY = self.size * 1/4
		for meep in range(5):
			for stack in range(self.meeples[meep]):
				pygame.draw.circle(gameDisplay, Tile.meepleColor[meep],   [x + cX, y + cY], self.size / 8)
				cX += self.size * 1/4
				if cX >= self.size:
					cX = self.size * 1/4
					cY += self.size * 1/4
					if cY >= self.size:
						cX = self.size * 3/8
						cY = self.size * 3/8


class Player:
	def __init__(self):
		self.coin = 0                   # current savings
		self.camels = 9                 # camels remaining
		self.whiteMeeples = 0           # accumulated white meeples
		self.yellowsMeeples = 0         # accumulated yellow meeples

class Board:
	def __init__(self):
		myPool = random.shuffle(Tile.availableTiles)

		self.tiles = [[Tile(myPool) for j in range(5)] for i in range(6)]
	def draw(self):
		for x in range(6):
			for y in range(5):
				self.tiles[x][y].draw(x = x * 110, y = y * 110)



#==============================================================================

def getResolvableTiles(radius = 0):
	retval = []
	xy_pairs = []
	if radius > 3 and radius % 2 == 0:
		xy_pairs = xy_pairs + [(0,0)]
	for rad in range(1, radius, 2):
		for itter in range(-rad, rad):
			xy_pairs = xy_pairs + [(itter, itter - abs(itter) )]  # /\
			if itter != -rad and itter != rad:
				xy_pairs = xy_pairs + [(itter, abs(itter) - itter )]  # /\

	return xy_pairs




def resolveTile(tile):
	return








#==============================================================================


pygame.init()

myBoard = Board()

gameDisplay = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Five Tribes Calculator')

gameExit = False

print getResolvableTiles(1)


while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				gameExit = True
 
	gameDisplay.fill((0,0,0))
	myBoard.draw()
	pygame.display.update()
 
pygame.quit()
quit()