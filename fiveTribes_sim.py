import pygame
import copy

class Tile:
	meepleColor = [
					(240,  0,  0),
					(0  ,230,  0),
					( 10, 10,250),
					(250,250,250),
					(240,240,  0),  ]
	meepleColorHash = {
					""       : ( 50, 50, 50),
					"none"   : ( 50, 50, 50),
					"red"    : (240,  0,  0),
					"green"  : (0  ,230,  0),
					"blue"   : ( 10, 10,250),
					"white"  : (250,250,250),
					"yellow" : (240,240,  0),}
	meepleColorText = [
					"red",
					"green",
					"blue",
					"white",
					"yellow",  ]
	tileColor = {"none":(50,50,50),"blue":(150,150,240), "red":(240,150,150)}
	size = 100
	sprites = {}

	def __init__(self, setup = ('none',0,'none')):
		#               r,g,b,w,y
		#self.meeples = [random.randrange(3),random.randrange(3),random.randrange(3),random.randrange(3),random.randrange(3)]
		self.meeples = [0,0,0,0,0]
		self.color = setup[0]
		self.value = setup[1]                  # victory point worth of the tile
		self.reward = setup[2]
		self.palmTrees = 0                     # accumulated palm trees
		self.village = 0                       # accumulated village
		self.camel = "none"                    # 'me', 'other'

	def draw(self, display, x, y, option = "none"):
		# background
		if option == "highlight_white":
			pygame.draw.rect(display, (255, 255, 255), [x,y,Tile.size,Tile.size], 5)
			pygame.draw.rect(display, (170, 170, 170), [x,y,Tile.size,Tile.size])
		if option == "highlight_red":
			pygame.draw.rect(display, (255, 0, 0), [x,y,Tile.size,Tile.size], 10)
			pygame.draw.rect(display, (200, 140, 140), [x,y,Tile.size,Tile.size])
		if option == "none":
			if self.value > 0:
				pygame.draw.rect(display, (100, 100, 100), [x,y,Tile.size,Tile.size])
			else:
				# for blank tile just draw grey circle
				pygame.draw.circle(display, (20, 20, 20), [x + Tile.size/2,y+Tile.size/2], Tile.size * 1/2)
		pygame.draw.circle(display, self.tileColor[self.color], [x + Tile.size * 9/10, y + Tile.size * 1/10], Tile.size / 10)
		# draw tile value text
		font = pygame.font.Font(None, Tile.size * 1/5)
		text = font.render(str(self.value), 1, (10,10,10))
		textpos = (
			-text.get_rect().center[0] + x + Tile.size * 9/10, 
			-text.get_rect().center[1] + y + Tile.size * 1/10)
		display.blit(text, textpos)

		# owner (camel)
		if self.camel != "none":
			sprite = pygame.transform.scale(Tile.sprites["camel"][Player.playerIndex[self.camel]], (Tile.size / 4, Tile.size / 4))
			display.blit(sprite, (x + Tile.size * 7/10, y + Tile.size * 1/10))

		# reward
		if self.reward == "palm":
			sprite = pygame.transform.scale(Tile.sprites["palm"], (Tile.size / 4, Tile.size / 4))
			display.blit(sprite, (x + Tile.size / 12, y + Tile.size * 8 / 12))
		if self.reward == "village":
			sprite = pygame.transform.scale(Tile.sprites["palace"], (Tile.size / 4, Tile.size / 4))
			display.blit(sprite, (x + Tile.size / 12, y + Tile.size * 8 / 12))

		# meeples
		cX = Tile.size * 1/8
		cY = Tile.size * 1/4
		for meep in range(5):
			for stack in range(self.meeples[meep]):
				#pygame.draw.circle(display, Tile.meepleColor[meep],   [x + cX, y + cY], Tile.size / 8)
				sprite = pygame.transform.scale(Tile.sprites["meeple"][meep], (Tile.size / 4, Tile.size / 4))
				display.blit(sprite, (x + cX - Tile.size / 8, y + cY - Tile.size / 8))
				cX += Tile.size * 1/4
				if cX >= Tile.size * 7/8:
					cX = cX - Tile.size * 6/8
					cY += Tile.size * 1/4
					if cY >= Tile.size:
						cX = cX + Tile.size * 1/8
						cY = Tile.size * 3/8

#==============================================================================


class Player:
	availablePlayers = \
		[["orange" , (243,155, 99)],\
		 ["blue"   , ( 53,191,204)],\
		 ["black"  , (100,100,100)],\
		 ["pink"   , (242,146,188)],]
	playerIndex = {
		"orange":0,
		"blue"  :1,
		"black" :2,
		"pink"  :3,}
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
		self.useSlaves = False
		self.slaves = 0                 # accumulated slave cards
		self.cardValue = [0, 1, 3, 7, 13, 21, 30, 40, 50, 60]
		self.cards_histo = [
			[0, "ivory"],
			[0, "jewels"],
			[0, "gold"],
			[0, "papyrus"],
			[0, "silk"],
			[0, "spice"],
			[0, "fish"],
			[0, "wheat"],
			[0, "pottery"]]
	def calcCardValue(self, cards_histo = []):
		retval = 0
		flag_done = False
		cards = copy.deepcopy(cards_histo)
		while not flag_done:
			cardinality = 0
			for card in cards:
				if card[0] > 0:
					cardinality = cardinality + 1
					card[0] = card[0] - 1
			if cardinality == 0:
				flag_done = True
			retval = retval + self.cardValue[cardinality]
		return retval





#==============================================================================


class Deck:
	availableCards = \
		["ivory", "jewels", "gold"]  * 2 + \
		["papyrus", "silk", "spice"] * 4 + \
		["fish", "wheat", "pottery"] * 6
	availableCards_histo = [
		[2, "ivory"],
		[2, "jewels"],
		[2, "gold"],
		[4, "papyrus"],
		[4, "silk"],
		[4, "spice"],
		[6, "fish"],
		[6, "wheat"],
		[6, "pottery"]]
	def __init__(self):
		self.stack = []

#==============================================================================


class Board:
	width = 6
	height = 5
	tileSpacing = 10
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

	def draw(self, display, highlights_white = [], highlights_red = []):
		for x in range(Board.width):
			for y in range(Board.height):
				option = "none"
				if (x, y) in highlights_white:
					option = "highlight_white"
				if (x, y) in highlights_red:
					option = "highlight_red"
				self.tiles[x][y].draw(display,
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
		for scanx in range(x-1, x+2):
			for scany in range(y-1, y+2):
				if self.checkInBounds(scanx, scany) == 1:
					if self.tiles[scanx][scany].color == "blue":
						retval = retval + 1
		return retval

	def resolveTile(self, player, deck, src = [], tile = [], meeples = []):
		x = tile[0]
		y = tile[1]
		targetTile = self.tiles[x][y]     # landing tile
		results = [0,0,0,0,0]             # scores per color
		isValidMove = [False,False,False,False,False]
		looping = [0,0,0,0,0]

		# looping
		for x in range(5):
			if meeples[x] > 1 and (abs(src[0] - tile[0]) + abs(src[1] - tile[1])) <= sum(meeples) - 4:
				looping[x] = looping[x] + 1


		#======================================================================
		#--- red ---
		if meeples[0] > 0 and (targetTile.meeples[0] + looping[0]) > 0:
			isValidMove[0] = True

		#======================================================================
		#--- green ---
		if meeples[1] > 0 and (targetTile.meeples[1] + looping[1]) > 0:
			cardsToTake = (targetTile.meeples[1] + looping[1]) + 1
			maxReturn = 0
			if len(deck.stack) > 0:
				# generate card options
				powerset = frozenset(map(frozenset, reduce(lambda result, x: result + [subset + [x] for subset in result], list(deck.stack), [[]])))
				powerset = [elem for elem in powerset if len(elem) <= cardsToTake]
				for combo in powerset:
					mergedList = copy.deepcopy(player.cards_histo)
					for elem in combo:
						for index in mergedList:
							if index[1] == elem:
								index[0] = index[0] + 1
					result = player.calcCardValue(mergedList)
					if result > maxReturn:
						maxReturn = result
			results[1] = maxReturn
			isValidMove[1] = True

		#======================================================================
		#--- blue ---
		if meeples[2] > 0 and (targetTile.meeples[2] + looping[2]) > 0:
			results[2] = self.countAdjacentBlueTiles(x, y) * (1 + (targetTile.meeples[2] + looping[2]) + int(player.useSlaves) * player.slaves)
			isValidMove[2] = True

		#======================================================================
		#--- white ---
		if meeples[3] > 0 and (targetTile.meeples[3] + looping[3]) > 0:
			results[3] = (1 + (targetTile.meeples[3] + looping[3])) * player.whiteMeepleValue
			isValidMove[3] = True

		#======================================================================
		#--- yellow ---
		if meeples[4] > 0 and (targetTile.meeples[4] + looping[4]) > 0:
			results[4] = (1 + (targetTile.meeples[4] + looping[4])) * player.yellowMeepleValue
			isValidMove[4] = True
		
		#======================================================================
		# tile value / village / palm tree
		bonus = 0
		if targetTile.camel == "none":
			bonus = bonus + targetTile.value
		if targetTile.camel == "none" or targetTile.camel == player.name:
			if targetTile.reward == "palm":
				bonus = bonus + player.palmValue
			if targetTile.reward == "village":
				bonus = bonus + player.villageValue
		for x in range(5):
			if isValidMove[x]:
				results[x] = results[x] + bonus

		return results

	def getResults_tile(self, player, deck, src = [], tiles = [], meeples = []):
		retval = []
		results = [self.resolveTile(player, deck, src, tile, meeples) + [tile[0], tile[1]] for tile in tiles]
		for tile in results:
			for x in range(5):
				retval = retval + [[tile[x], Tile.meepleColorText[x], (tile[5], tile[6])]]
		#return sorted(retval, key= lambda tup: tup[0], reverse= True)
		return retval

	def getResults_board(self, player, deck):
		retval = []
		for scanx in range(self.width):
			for scany in range(self.height):
				tiles = self.getResolvableTiles(x=scanx, y=scany, radius= sum(self.tiles[scanx][scany].meeples) + 1)
				results = self.getResults_tile(player=player, deck = deck, src=[scanx, scany], tiles=tiles, meeples=self.tiles[scanx][scany].meeples)
				for res in results:
					res.insert(2, (scanx, scany))
					retval = retval + [res]

		return sorted(retval, key= lambda tup: tup[0], reverse= True)


#==============================================================================

