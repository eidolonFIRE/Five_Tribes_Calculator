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
	meepleColorText = [
					"red",
					"green",
					"blue",
					"white",
					"yellow",  ]
	size = 100

	def __init__(self, setup):
		#               r,g,b,w,y
		self.meeples = [random.randrange(2),random.randrange(2),random.randrange(2),random.randrange(2),random.randrange(2)]
		#self.meeples = [2,0,0,0,0]
		self.color = setup[0]        
		self.value = setup[1]                  # victory point worth of the tile
		self.reward = setup[2]
		self.palmTrees = 0                     # accumulated palm trees
		self.village = 0                       # accumulated village
		self.camel = 'none'                    # 'me', 'other'


	def draw(self, x, y, option = "none"):
		# background
		if option == "highlight_white":
			pygame.draw.rect(gameDisplay, (255, 255, 255), [x,y,Tile.size,Tile.size], 5)
			pygame.draw.rect(gameDisplay, (170, 170, 170), [x,y,Tile.size,Tile.size])
		if option == "highlight_red":
			pygame.draw.rect(gameDisplay, (255, 0, 0), [x,y,Tile.size,Tile.size], 10)
			pygame.draw.rect(gameDisplay, (200, 140, 140), [x,y,Tile.size,Tile.size])
		if option == "none":
			pygame.draw.rect(gameDisplay, (100, 100, 100), [x,y,Tile.size,Tile.size])
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
	def __init__(self, name):
		self.name = name
		self.coin = 0                   # current savings
		self.camels = 9                 # camels remaining
		self.whiteMeeples = 0           # accumulated white meeples
		self.yellowsMeeples = 0         # accumulated yellow meeples
		self.yellowMeepleValue = 1
		self.whiteMeepleValue = 2
		self.villageValue = 5
		self.palmValue = 3

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
	def draw(self, highlights_white = [], highlights_red = []):
		for x in range(Board.width):
			for y in range(Board.height):
				option = "none"
				if (x, y) in highlights_white:
					option = "highlight_white"
				if (x, y) in highlights_red:
					option = "highlight_red"
				self.tiles[x][y].draw(
					x = x * (Tile.size + Board.tileSpacing), 
					y = y * (Tile.size + Board.tileSpacing),
					option = option)

	def getTileChord(self, pos):
		return (pos[0] / (Tile.size + self.tileSpacing), pos[1] / (Tile.size + self.tileSpacing))

	def clickTile(self, tileX, tileY):
		retval = 0
		# if selection is within bounds
		if tileX >= 0 and tileX < Board.width and tileY >= 0 and tileY < Board.height:
			retval = self.getResolvableTiles(x=tileX, y=tileY, radius= sum(self.tiles[tileX][tileY].meeples) + 1)
		return retval

	def getResolvableTiles(self, x = 0, y = 0, radius = 0):
		xy_pairs = []
		
		for scanx in range(0, radius):
			for scany in range(0, radius):
				if scanx == 0 and scany == 0:
					continue
				if (scanx + scany + radius + 1) % 2 == 0 and (scanx + scany) <= radius:
					xy_pairs = xy_pairs + [(x + scanx, y + scany)]
					if scanx != 0:
						xy_pairs = xy_pairs + [(x - scanx, y + scany)]
					if scany != 0:
						xy_pairs = xy_pairs + [(x + scanx, y - scany)]
					if scanx != 0 and scany !=0:
						xy_pairs = xy_pairs + [(x - scanx, y - scany)]
		if (radius + 1) % 2 == 0 and radius > 3:
			xy_pairs = xy_pairs + [(x, y)]

		# clean up pairs
		retval = []
		for pair in xy_pairs:
			if self.checkInBounds(pair[0], pair[1]) == 1:
				retval = retval + [pair]
		return retval

	def checkInBounds(self, x, y):
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			return 1
		else:
			return 0

	def countAdjacentBlueTiles(self, x, y):
		retval = 0
		for scanx in range(-1, 1):
			for scany in range(-1, 1):
				if scanx == 0 and scany == 0:
					continue
				if self.checkInBounds(scanx, scany) == 1:
					if self.tiles[scanx][scany].color == "blue":
						retval = retval + 1
		return retval

	def resolveTile(self, player, tile = [], meeples = []):
		x = tile[0]
		y = tile[1]
		targetTile = self.tiles[x][y]     # landing tile
		results = [0,0,0,0,0]             # scores per color

		# red
		#if meeples[0] > 0:
		# green
		#if meeples[1] > 0:
		# blue
		if meeples[2] > 0:
			results[2] = self.countAdjacentBlueTiles(x, y) * (meeples[2] + targetTile.meeples[2])
		# white
		if meeples[3] > 0:
			results[3] = (meeples[3] + targetTile.meeples[3]) * player.whiteMeepleValue
		# yellow
		if meeples[4] > 0:
			results[4] = (meeples[4] + targetTile.meeples[4]) * player.yellowMeepleValue
		
		# tile value / village / palm tree
		bonus = 0
		if targetTile.camel == "none":
			bonus = bonus + targetTile.value
		if targetTile.camel == "none" or targetTile.camel == player.name:
			if targetTile.reward == "palm":
				bonus = bonus + player.palmValue
			if targetTile.reward == "village":
				bonus = bonus + player.villageValue
		results = [x + bonus for x in results]

		return results

	def getResults_tile(self, player, tiles = [], meeples = []):
		retval = []
		results = [self.resolveTile(player, tile, meeples) + [tile[0], tile[1]] for tile in tiles]
		for tile in results:
			for x in range(5):
				retval = retval + [[tile[x], Tile.meepleColorText[x], (tile[5], tile[6])]]
		#return sorted(retval, key= lambda tup: tup[0], reverse= True)
		return retval

	def getResults_board(self, player):
		retval = []
		for scanx in range(self.width):
			for scany in range(self.height):
				tiles = self.getResolvableTiles(x=scanx, y=scany, radius= sum(self.tiles[scanx][scany].meeples) + 1)
				results = self.getResults_tile(player=player, tiles=tiles, meeples=self.tiles[scanx][scany].meeples)
				for res in results:
					res.insert(2, (scanx, scany))
					retval = retval + [res]

		return sorted(retval, key= lambda tup: tup[0], reverse= True)


#==============================================================================


class Button:
	def __init__(self, x, y, w, h, color, text, shape, method_click):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color
		self.text = text
		self.shape = shape
		self.method_click = method_click
	def draw(self):
		if self.shape == "rect":
			pygame.draw.rect(gameDisplay, self.color, [self.x,self.y,self.w,self.h])
		if self.shape == "ellipse":
			pygame.draw.circ(gameDisplay, self.color, [self.x,self.y,self.w,self.h])
		font = pygame.font.Font(None, Tile.size * 1/5)
		text = font.render(self.text, 1, (0,0,0))
		textpos = (
			-text.get_rect().center[0] + self.x + self.w * 5/10, 
			-text.get_rect().center[1] + self.y + self.h * 5/10)
		gameDisplay.blit(text, textpos)
	def down(self):
		self.method_click()


class GUI:
	def __init__(self):
		self.buttons = []
	def draw(self):
		for butt in self.buttons:
			butt.draw()
	def addButton(self, x, y, w, h, color, text, shape, method_click):
		self.buttons = self.buttons + [Button(x, y, w, h, color, text, shape, method_click)]
	def mouseDown(self, pos):
		for butt in self.buttons:
			if pos[0] > butt.x \
			and pos[0] < butt.x + butt.w \
			and pos[1] > butt.y \
			and pos[1] < butt.y + butt.h:
				butt.down()



#==============================================================================

def changeMode():
	print "mode changed"

def solve():
	results = myBoard.getResults_board(myPlayer)
	print "--- board results ---"
	for x in results[0:15]:
		print resultText.format(score=x[0], color=x[1], sx=x[2][0], sy=x[2][1], tx=x[3][0], ty=x[3][1])


#==============================================================================


resultText = "{score:>2} {color:6} from: {sx:1},{sy:1} --> to: {tx:1},{ty:1}"

pygame.init()

myGui = GUI()
myBoard = Board()
myPlayer = Player("Player1")
selectedTile = (0,0)

gameDisplay = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Five Tribes Calculator')

gameExit = False
highlights = []

myGui.addButton(660, 20, 80, 30, (150,150,150), "test", "rect", changeMode)
myGui.addButton(660, 60, 80, 30, (150,150,150), "solve", "rect", solve)


while not gameExit:
	event = pygame.event.wait()
	#for event in pygame.event.get():
	if event.type == pygame.QUIT:
		gameExit = True
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_q:
			gameExit = True
	if event.type == pygame.MOUSEBUTTONDOWN:
		selectedTile = myBoard.getTileChord(pygame.mouse.get_pos())
		myGui.mouseDown(pygame.mouse.get_pos())

	if event.type != pygame.MOUSEMOTION:

		gameDisplay.fill((0,0,0))
		myBoard.draw(highlights_white = highlights, highlights_red = [selectedTile])
		myGui.draw()
		pygame.display.update()

pygame.quit()
quit()