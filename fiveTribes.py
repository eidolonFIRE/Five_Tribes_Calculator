import pygame
import math
import random
import os
from fiveTribes_sim import Tile, Board, Player, Deck
from gui import GUI, Button, List, ValueBox, CheckBox

# Manual
# http://cdn0.daysofwonder.com/five-tribes/en/img/ft_rules_en.pdf



# TODO
# - red meeples!
# - calculate merchants
# - real-time scalable GUI









#==============================================================================
#    Global handlers
#
#------------------------------------------------------------------------------

def mode_cards():
	global myPlayer
	myGui.objects["player_cards_select"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myPlayer.cards_histo]
	myGui.objects["player_cards_value"].text = [" Value: " + str(myPlayer.calcCardValue(myPlayer.cards_histo))]
	myGui.mode = "player"

def player_cards_select(index = 0, x = 0):
	global myPlayer
	if x < 0:
		if myPlayer.cards_histo[index][0] > 0:
			myPlayer.cards_histo[index][0] = myPlayer.cards_histo[index][0] - 1
			myGui.objects["player_cards_select"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myPlayer.cards_histo]
			myGui.objects["player_cards_value"].text = [" Value: " + str(myPlayer.calcCardValue(myPlayer.cards_histo))]
	else:
		myPlayer.cards_histo[index][0] = myPlayer.cards_histo[index][0] + 1
		myGui.objects["player_cards_select"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myPlayer.cards_histo]
		myGui.objects["player_cards_value"].text = [" Value: " + str(myPlayer.calcCardValue(myPlayer.cards_histo))]

def setSlaves(value = 0):
	global myPlayer
	myPlayer.slaves = value

def selectPlayerColor(index = 0, x = 0):
	camel = Player.availablePlayers[index][0]
	myPlayer.color = camel
	myGui.objects["player_color"].text = [[("X) " if x[0] == camel else " ) ") + x[0], x[1]] for x in Player.availablePlayers]



def mode_deck():
	myGui.objects["deckAdd"].text = [str(x[0]) + " " + str(x[1]) for x in myDeck.availableCards_histo]
	myGui.objects["deck"].text = [deckText.format(text = x) for x in myDeck.stack]
	myGui.mode = "deck"

def deckAdd(index = 0, x = 0):
	if len(myDeck.stack) < 9:
		myDeck.stack = myDeck.stack + [myDeck.availableCards_histo[index][1]]
		myDeck.availableCards_histo[index][0] = myDeck.availableCards_histo[index][0] - 1
		myGui.objects["deckAdd"].text = [str(x[0]) + " " + str(x[1]) for x in myDeck.availableCards_histo]
		myGui.objects["deck"].text = [deckText.format(text = x) for x in myDeck.stack]

def deckPop(index = 0, x = 0):
	myDeck.stack.pop(index)
	myGui.objects["deck"].text = [deckText.format(text = x) for x in myDeck.stack]



def mode_board():
	global highlights_white
	global highlights_red
	highlights_white = []
	highlights_red = []
	myGui.mode = "board"

def selectOwnership(index = 0, x = 0):
	global selectedTile
	camel = Player.availablePlayers[index][0]
	myBoard.tiles[selectedTile[0]][selectedTile[1]].camel = camel
	myGui.objects["ownership"].text = [[("X) " if x[0] == camel else " ) ") + x[0], x[1]] for x in Player.availablePlayers]



def mode_solve():
	textResults = []
	myGui.mode = "solve"
	global solvedResults
	solvedResults = myBoard.getResults_board(myPlayer, myDeck)
	#print "--- board results ---"
	for x in solvedResults[0:20]:
		result = resultText.format(score=x[0], color=x[1], sx=x[2][0], sy=x[2][1], tx=x[3][0], ty=x[3][1])
		textResults = textResults + [[result, Tile.meepleColorHash[x[1]]]]
		#print result
	myGui.objects["solve_results"].text = textResults

def setUseSlaves(value = False):
	global myPlayer
	myPlayer.useSlaves = value
	mode_solve()

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

def selectTile(index = 0, x = 0):
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
	camel = myBoard.tiles[selectedTile[0]][selectedTile[1]].camel
	myGui.objects["ownership"].text = [[("X) " if x[0] == camel else " ) ") + x[0], x[1]] for x in Player.availablePlayers]



def clearTile():
	global selectedTile
	x = selectedTile[0]
	y = selectedTile[1]
	selTile = myBoard.tiles[x][y]
	if selTile.value > 0:
		# restore available tile back to list
		for histTile in myBoard.availableTiles_histo:
			if selTile.color == histTile[1] \
			and selTile.value == histTile[2] \
			and selTile.reward == histTile[3]:
				histTile[0] = histTile[0] + 1
				break
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

def colorize(image, newColor):
	image = image.convert()
	image.fill(newColor[0:3] + (255,), None, pygame.BLEND_RGBA_MULT)
	image.set_colorkey((0,0,0))
	return image


#==============================================================================
#    Init
#
#------------------------------------------------------------------------------


resultText = " {score:>2} {color:6} {sx:1},{sy:1} > {tx:1},{ty:1}"
tileText = " {remaining:1}) {color:4} {value:>2} {reward:8}"
cardText = "<{remaining:1}) {card:7}>"
deckText = " {text:9} X"

pygame.init()
myDisplay = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Five Tribes Calculator')
simExit = False

myGui = GUI(myDisplay)
myGui.mode = "board"
myBoard = Board()
myPlayer = Player("Player1")
myDeck = Deck()

selectedTile = (0,0)
highlights_white = []
highlights_red = []
solvedResults = []

# sprites
meepSprites = []
for meep in Tile.meepleColor:
	meepSprites = meepSprites + [colorize(pygame.image.load(os.path.join('images', 'meeple.bmp')), meep )]
Tile.sprites["meeple"] = meepSprites
Tile.sprites["palm"]   = colorize(pygame.image.load(os.path.join('images', 'palm_masked.png')), (255,255,255))
Tile.sprites["palace"] = colorize(pygame.image.load(os.path.join('images', 'palace_masked.png')), (255,255,255))
camelSprites = []
for player in Player.availablePlayers:
	camelSprites = camelSprites + [colorize(pygame.image.load(os.path.join('images', 'camel.bmp')), player[1] )]
Tile.sprites["camel"] = camelSprites

# solve mode
myGui.objects["modeSolve"]       =   Button(pygame.Rect(730,  10,  60,  25), (150,150,150), "Solve", 20, "rect", mode_solve, ["all"])
myGui.objects["solve_results"]   =     List(pygame.Rect(660,  70, 250, 500), (250,250,250), solvedResults, 20, selectResult, ["solve"])
myGui.objects["solve_useSlaves"] = CheckBox(pygame.Rect(660,  40, 160,  20), (100,100,100), False, "Use Slaves", 20, setUseSlaves, ["solve"])

# board mode
myGui.objects["modeBoard"] =   Button(pygame.Rect(660,  10,  60,  25), (150,150,150), "Edit", 20, "rect", mode_board, ["all"])
myGui.objects["clearTile"] =   Button(pygame.Rect(660,  40, 100,  25), (150,150,150), "Clear Tile", 20, "rect", clearTile, ["board"])
myGui.objects["tiles"]     =     List(pygame.Rect(660, 200, 250, 180), (250,250,250), ["..."], 20, selectTile, ["board"])
myGui.objects["reds"]      = ValueBox(pygame.Rect(660,  70, 110,  20), (255,100,100), (0,10), 20, setReds, ["board"])
myGui.objects["greens"]    = ValueBox(pygame.Rect(660,  95, 110,  20), (100,255,100), (0,10), 20, setGreens, ["board"])
myGui.objects["blues"]     = ValueBox(pygame.Rect(660, 120, 110,  20), (100,100,255), (0,10), 20, setBlues, ["board"])
myGui.objects["whites"]    = ValueBox(pygame.Rect(660, 145, 110,  20), (255,255,255), (0,10), 20, setWhites, ["board"])
myGui.objects["yellows"]   = ValueBox(pygame.Rect(660, 170, 110,  20), (255,242,  0), (0,10), 20, setYellows, ["board"])
myGui.objects["ownership"] =     List(pygame.Rect(780,  70, 130, 100), (100,100,100), [["-) "  + x[0], x[1]] for x in Player.availablePlayers], 20, selectOwnership, ["board"])

# player mode
myGui.objects["modeCards"]            =   Button(pygame.Rect(800,  10,  60,  25), (150,150,150), "Cards", 20, "rect", mode_cards, ["all"])
myGui.objects["player_cards_select"]  =     List(pygame.Rect(660, 250, 160, 200), (250,250,250), ["..."], 20, player_cards_select, ["player"])
myGui.objects["player_cards_value"]   =     List(pygame.Rect(660, 220, 160,  40), (250,250,250), ["..."], 20, None, ["player"])
myGui.objects["player_slaves_slaves"] =   Button(pygame.Rect(660, 160, 160,  20), (100,100,100), "Slave Cards", 20, "rect", None, ["player"])
myGui.objects["player_slaves"]        = ValueBox(pygame.Rect(660, 180, 160,  20), (100,100,100), (0, 10), 20, setSlaves, ["player"])
myGui.objects["player_color"]         =     List(pygame.Rect(660,  40, 130, 100), (100,100,100), [["-) "  + x[0], x[1]] for x in Player.availablePlayers], 20, selectPlayerColor, ["player"])


# deck mode
myGui.objects["modeDeck"]  = Button(pygame.Rect(870,  10,  60,  25), (150,150,150), "Deck", 20, "rect", mode_deck, ["all"])
myGui.objects["deckAdd"]   =   List(pygame.Rect(660, 100, 160, 200), (250,250,250), ["..."], 20, deckAdd, ["deck"])
myGui.objects["deck"]      =   List(pygame.Rect(660, 310, 160, 200), (250,250,250), ["..."], 20, deckPop, ["deck"])




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
		if myGui.mode == "board":
			myGui.objects["tiles"].text = [[tileText.format(remaining=x[0], color=x[1], value=x[2], reward=x[3]), Tile.tileColor[x[1] if (x[0] > 0) else "none"]] for x in Board.availableTiles_histo]

		myDisplay.fill((0,0,0))
		myBoard.draw(myDisplay, highlights_white = highlights_white, highlights_red = highlights_red)
		myGui.draw()
		pygame.display.update()

pygame.quit()
quit()