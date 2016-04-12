import pygame
import math
import random
from gui import GUI

# Manual
# http://cdn0.daysofwonder.com/five-tribes/en/img/ft_rules_en.pdf

# NOTES ON MEEPLE PLACEMENT
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

# TODO -
# - slaves can be sold to increase blue factor
# - reds
# - calculate cards / merchants
# - reorganize some OOP things





#==============================================================================


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

	def __init__(self, setup = ('none',0,'none')):
		#               r,g,b,w,y
		#self.meeples = [random.randrange(3),random.randrange(3),random.randrange(3),random.randrange(3),random.randrange(3)]
		self.meeples = [0,0,0,0,0]
		self.color = setup[0]        
		self.value = setup[1]                  # victory point worth of the tile
		self.reward = setup[2]
		self.palmTrees = 0                     # accumulated palm trees
		self.village = 0                       # accumulated village
		self.camel = 'none'                    # 'me', 'other'


	def draw(self, x, y, option = "none"):
		# background
		if option == "highlight_white":
			pygame.draw.rect(myDisplay, (255, 255, 255), [x,y,Tile.size,Tile.size], 5)
			pygame.draw.rect(myDisplay, (170, 170, 170), [x,y,Tile.size,Tile.size])
		if option == "highlight_red":
			pygame.draw.rect(myDisplay, (255, 0, 0), [x,y,Tile.size,Tile.size], 10)
			pygame.draw.rect(myDisplay, (200, 140, 140), [x,y,Tile.size,Tile.size])
		if option == "none":
			if self.value > 0:
				pygame.draw.rect(myDisplay, (100, 100, 100), [x,y,Tile.size,Tile.size])
			else:
				# for blank tile just draw grey circle
				pygame.draw.circle(myDisplay, (20, 20, 20), [x + Tile.size/2,y+Tile.size/2], Tile.size * 1/2)
		if self.color == 'blue':
			pygame.draw.circle(myDisplay, (150,150,240), [x + Tile.size * 9/10, y + Tile.size * 1/10], Tile.size / 10)
		if self.color == 'red':
			pygame.draw.circle(myDisplay, (240,150,150), [x + Tile.size * 9/10, y + Tile.size * 1/10], Tile.size / 10)
		# draw tile value text
		font = pygame.font.Font(None, Tile.size * 1/5)
		text = font.render(str(self.value), 1, (10,10,10))
		textpos = (
			-text.get_rect().center[0] + x + Tile.size * 9/10, 
			-text.get_rect().center[1] + y + Tile.size * 1/10)
		myDisplay.blit(text, textpos)

		# meeples
		cX = Tile.size * 1/4
		cY = Tile.size * 1/4
		for meep in range(5):
			for stack in range(self.meeples[meep]):
				pygame.draw.circle(myDisplay, Tile.meepleColor[meep],   [x + cX, y + cY], Tile.size / 8)
				cX += Tile.size * 1/4
				if cX >= Tile.size:
					cX = Tile.size * 1/4
					cY += Tile.size * 1/4
					if cY >= Tile.size:
						cX = Tile.size * 3/8
						cY = Tile.size * 3/8

#==============================================================================


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
		self.cardValue = [0, 1, 3, 7, 13, 21, 30, 40, 50, 60]

#==============================================================================


class Deck:
	availableCards = \
	["ivory", "jewels", "gold"]  * 2 + \
	["papyrus", "silk", "spice"] * 4 + \
	["fish", "wheat", "pottery"] * 6


#==============================================================================


class Board:
	width = 6
	height = 5
	tileSpacing = 10
	availableTiles = \
		[('blue', 5 , 'village')] * 5 + \
		[('blue', 6 , 'djinn')  ] * 4 + \
		[('blue', 10, 'djinn')  ]     + \
		[('blue', 12, 'djinn')  ]     + \
		[('blue', 15, 'djinn')  ]     + \
		[('red', 4, 'l_market') ] * 4 + \
		[('red', 6, 's_market') ] * 8 + \
		[('red', 8, 'palm')     ] * 6
	availableTiles_histo = \
		[[5, 'blue',  5, 'village' ]] + \
		[[4, 'blue',  6, 'djinn'   ]] + \
		[[1, 'blue', 10, 'djinn'   ]] + \
		[[1, 'blue', 12, 'djinn'   ]] + \
		[[1, 'blue', 15, 'djinn'   ]] + \
		[[4, 'red' ,  4, 'l_market']] + \
		[[8, 'red' ,  6, 's_market']] + \
		[[6, 'red' ,  8, 'palm'    ]]
	availableMeeples_histo = [18,18,18,20,16]
	availablePalms = 12
	availablePalaces = 10

	def __init__(self):
		self.tiles = [[Tile() for j in range(Board.height)] for i in range(Board.width)]

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

	def clearTile(self, pos):
		self.tiles[pos[0]][pos[1]] = Tile()

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
		for scanx in range(x-1, x+1):
			for scany in range(y-1, y+1):
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
		#if meeples[0] > 0 and targetTile.meeples[0] > 0:
		# green
		#if meeples[1] > 0 and targetTile.meeples[1] > 0:
		# blue
		if meeples[2] > 0 and targetTile.meeples[2] > 0:
			results[2] = self.countAdjacentBlueTiles(x, y) * (meeples[2] + targetTile.meeples[2])
		# white
		if meeples[3] > 0 and targetTile.meeples[3] > 0:
			results[3] = (meeples[3] + targetTile.meeples[3]) * player.whiteMeepleValue
		# yellow
		if meeples[4] > 0 and targetTile.meeples[4] > 0:
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




#==============================================================================
#    Global handlers
#
#------------------------------------------------------------------------------

def mode_edit():
	global highlights_white
	global highlights_red
	highlights_white = []
	highlights_red = []
	myGui.mode = "edit"

def mode_solve():
	textResults = []
	myGui.mode = "solve"
	global solvedResults
	solvedResults = myBoard.getResults_board(myPlayer)
	print "--- board results ---"
	for x in solvedResults[0:20]:
		result = resultText.format(score=x[0], color=x[1], sx=x[2][0], sy=x[2][1], tx=x[3][0], ty=x[3][1])
		textResults = textResults + [result]
		print result
	myGui.objects["results"].text = textResults

def selectResult(x = 0):
	global solvedResults
	global highlights_white
	global highlights_red
	global resultText
	res = solvedResults[x]

	highlights_white = [tuple(res[2])]
	highlights_red = [tuple(res[3])]

	print "selected: " + str(x)
	print resultText.format(score=res[0], color=res[1], sx=res[2][0], sy=res[2][1], tx=res[3][0], ty=res[3][1])

def selectTile(index = 0):
	global selectedTile
	x = selectedTile[0]
	y = selectedTile[1]
	newTile = myBoard.availableTiles_histo[index]
	selTile = myBoard.tiles[x][y]
	if newTile[0] > 0:
		if selTile.value > 0:
			# restore available tile back to list
			for histTile in myBoard.availableTiles_histo:
				if selTile.color == histTile[1] \
				and selTile.value == histTile[2] \
				and selTile.reward == histTile[3]:
					histTile[0] = histTile[0] + 1
					break
		# load tile from list
		newTile[0] = newTile[0] - 1
		selTile.color = newTile[1]
		selTile.value = newTile[2]
		selTile.reward = newTile[3]

def setSelectedTile(pos):
	global selectedTile
	selectedTile = pos
	selTile = myBoard.tiles[pos[0]][pos[1]]
	myGui.objects["reds"   ].value = selTile.meeples[0]
	myGui.objects["greens" ].value = selTile.meeples[1]
	myGui.objects["blues"  ].value = selTile.meeples[2]
	myGui.objects["whites" ].value = selTile.meeples[3]
	myGui.objects["yellows"].value = selTile.meeples[4]


def clearTile():
	global selectedTile
	myBoard.clearTile(selectedTile)

def setReds(value = 0):
	global selectedTile
	myBoard.tiles[selectedTile[0]][selectedTile[1]].meeples[0] = value

def setGreens(value = 0):
	global selectedTile
	myBoard.tiles[selectedTile[0]][selectedTile[1]].meeples[1] = value

def setBlues(value = 0):
	global selectedTile
	myBoard.tiles[selectedTile[0]][selectedTile[1]].meeples[2] = value

def setWhites(value = 0):
	global selectedTile
	myBoard.tiles[selectedTile[0]][selectedTile[1]].meeples[3] = value

def setYellows(value = 0):
	global selectedTile
	myBoard.tiles[selectedTile[0]][selectedTile[1]].meeples[4] = value


#==============================================================================
#    Init
#
#------------------------------------------------------------------------------


resultText = "{score:>2} {color:6} {sx:1},{sy:1} --> {tx:1},{ty:1}"
tileText = "{remaining:1}) {color:4} {value:>2} {reward:8}"

pygame.init()
myDisplay = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Five Tribes Calculator')
simExit = False

myGui = GUI(myDisplay)
myBoard = Board()
myPlayer = Player("Player1")
selectedTile = (0,0)
highlights_white = []
highlights_red = []
solvedResults = []

# main buttons
myGui.addButton("modeEdit", (660, 10, 60, 25), (150,150,150), "Edit", 20, "rect", mode_edit, ["edit", "solve"])
myGui.addButton("modeSolve", (730, 10, 60, 25), (150,150,150), "Solve", 20, "rect", mode_solve, ["edit", "solve"])

# solve mode
myGui.addList("results", (660, 40, 200, 600), (250, 250, 250), solvedResults, 20, selectResult, ["solve"])

# edit mode
myGui.addButton("clearTile", (660, 50, 60, 25), (150,150,150), "Clear Tile", 20, "rect", clearTile, ["edit"])
myGui.addList("tiles", (660, 200, 200, 180), (250, 250, 250), [tileText.format(remaining=x[0], color=x[1], value=x[2], reward=x[3]) for x in Board.availableTiles_histo], size = 20, method_select = selectTile, layers = ["edit"])
myGui.addValueBox("reds"   , (660,  80, 100, 20), (255,100,100), (0,10), 20, setReds, ["edit"])
myGui.addValueBox("greens" , (660, 100, 100, 20), (100,255,100), (0,10), 20, setGreens, ["edit"])
myGui.addValueBox("blues"  , (660, 120, 100, 20), (100,100,255), (0,10), 20, setBlues, ["edit"])
myGui.addValueBox("whites" , (660, 140, 100, 20), (255,255,255), (0,10), 20, setWhites, ["edit"])
myGui.addValueBox("yellows", (660, 160, 100, 20), (255,242,  0), (0,10), 20, setYellows, ["edit"])


#==============================================================================
#    Main loop
#
#------------------------------------------------------------------------------


while not simExit:
	event = pygame.event.wait()
	#for event in pygame.event.get():
	if event.type == pygame.QUIT:
		simExit = True
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_q:
			simExit = True
	if event.type == pygame.MOUSEBUTTONDOWN:
		pos = myBoard.getTileChord(pygame.mouse.get_pos())
		if myBoard.checkInBounds(pos[0],pos[1]) == 1:
			setSelectedTile(pos)
		myGui.mouseDown(pygame.mouse.get_pos())

	if event.type != pygame.MOUSEMOTION:

		highlights_red = [selectedTile]
		if myGui.mode == "edit":
			myGui.objects["tiles"].text = [tileText.format(remaining=x[0], color=x[1], value=x[2], reward=x[3]) for x in Board.availableTiles_histo]

		myDisplay.fill((0,0,0))
		myBoard.draw(highlights_white = highlights_white, highlights_red = highlights_red)
		myGui.draw()
		pygame.display.update()

pygame.quit()
quit()