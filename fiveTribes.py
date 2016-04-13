import pygame
import math
import random
import os
from fiveTribes_sim import Tile, Board, Player, Deck
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
#    Global handlers
#
#------------------------------------------------------------------------------

def mode_cards():
	global myPlayer
	myGui.objects["cards_player_decr"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myPlayer.cards_histo]
	myGui.mode = "cards"

def cards_decr(index = 0):
	global myPlayer
	if myPlayer.cards_histo[index][0] > 0:
		myPlayer.cards_histo[index][0] = myPlayer.cards_histo[index][0] - 1
		myGui.objects["cards_player_decr"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myPlayer.cards_histo]
		print "card score: " + str(myPlayer.calcCardValue(myPlayer.cards_histo))

def cards_incr(index = 0):
	global myPlayer
	myPlayer.cards_histo[index][0] = myPlayer.cards_histo[index][0] + 1
	myGui.objects["cards_player_decr"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myPlayer.cards_histo]
	print "card score: " + str(myPlayer.calcCardValue(myPlayer.cards_histo))




def mode_deck():
	myGui.objects["deck_decr"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myDeck.availableCards_histo]
	myGui.objects["deck"].text = myDeck.stack
	myGui.mode = "deck"

def deck_decr(index = 0):
	if len(myDeck.stack) > 0 and Deck.availableCards_histo[index][1] in myDeck.stack:
		myDeck.stack.remove(Deck.availableCards_histo[index][1])
		myGui.objects["deck_decr"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myDeck.availableCards_histo]
		myGui.objects["deck"].text = myDeck.stack

def deck_incr(index = 0):
	if len(myDeck.stack) < 9:
		myDeck.stack = myDeck.stack + [Deck.availableCards_histo[index][1]]
		myGui.objects["deck_decr"].text = [cardText.format(remaining = x[0], card = x[1]) for x in myDeck.availableCards_histo]
		myGui.objects["deck"].text = myDeck.stack




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
	solvedResults = myBoard.getResults_board(myPlayer, myDeck)
	#print "--- board results ---"
	for x in solvedResults[0:20]:
		result = resultText.format(score=x[0], color=x[1], sx=x[2][0], sy=x[2][1], tx=x[3][0], ty=x[3][1])
		textResults = textResults + [result]
		#print result
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

def colorize(image, newColor):
	image = image.convert()
	image.fill(newColor[0:3] + (255,), None, pygame.BLEND_RGBA_MULT)
	image.set_colorkey((0,0,0))
	return image


#==============================================================================
#    Init
#
#------------------------------------------------------------------------------


resultText = "{score:>2} {color:6} {sx:1},{sy:1} --> {tx:1},{ty:1}"
tileText = "{remaining:1}) {color:4} {value:>2} {reward:8}"
cardText = "{remaining:1}) {card:7}"

pygame.init()
myDisplay = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Five Tribes Calculator')
simExit = False

myGui = GUI(myDisplay)
myBoard = Board()
myPlayer = Player("Player1")
myDeck = Deck()

selectedTile = (0,0)
highlights_white = []
highlights_red = []
solvedResults = []

# sprites
meepSprites = []
for meep in range(5):
	meepSprites = meepSprites + [colorize(pygame.image.load(os.path.join('images', 'meeple_masked.png')), Tile.meepleColor[meep] )]
Tile.sprites["meeple"] = meepSprites
Tile.sprites["palm"] = colorize(pygame.image.load(os.path.join('images', 'palm_masked.png')), (255,255,255))
Tile.sprites["palace"] = colorize(pygame.image.load(os.path.join('images', 'palace_masked.png')), (255,255,255))


# main buttons
myGui.addButton("modeEdit", (660, 10, 60, 25), (150,150,150), "Edit", 20, "rect", mode_edit, ["all"])
myGui.addButton("modeSolve", (730, 10, 60, 25), (150,150,150), "Solve", 20, "rect", mode_solve, ["all"])

# solve mode
myGui.addList("results", (660, 40, 250, 500), (250, 250, 250), solvedResults, 20, selectResult, ["solve"])

# edit mode
myGui.addButton("clearTile", (660, 40, 100, 25), (150,150,150), "Clear Tile", 20, "rect", clearTile, ["edit"])
myGui.addList("tiles", (660, 200, 250, 180), (250, 250, 250), ["..."], 20, selectTile, ["edit"])
myGui.addValueBox("reds"   , (660,  70, 100, 20), (255,100,100), (0,10), 20, setReds, ["edit"])
myGui.addValueBox("greens" , (660,  95, 100, 20), (100,255,100), (0,10), 20, setGreens, ["edit"])
myGui.addValueBox("blues"  , (660, 120, 100, 20), (100,100,255), (0,10), 20, setBlues, ["edit"])
myGui.addValueBox("whites" , (660, 145, 100, 20), (255,255,255), (0,10), 20, setWhites, ["edit"])
myGui.addValueBox("yellows", (660, 170, 100, 20), (255,242,  0), (0,10), 20, setYellows, ["edit"])

# cards mode
myGui.addButton("modeCards", (800, 10, 60, 25), (150,150,150), "Cards", 20, "rect", mode_cards, ["all"])
myGui.addList("cards_player_decr", (660, 200, 80, 200), (250, 250, 250), ["..."], 20, cards_decr, ["cards"])
myGui.addList("cards_player_incr", (740, 200, 80, 200), (250, 250, 250), ["","","","","","","","",""], 20, cards_incr, ["cards"])

# deck mode
myGui.addButton("modeDeck", (870, 10, 60, 25), (150,150,150), "Deck", 20, "rect", mode_deck, ["all"])
myGui.addList("deck_decr", (660, 200, 80, 200), (250, 250, 250), ["..."], 20, deck_decr, ["deck"])
myGui.addList("deck_incr", (740, 200, 80, 200), (250, 250, 250), ["","","","","","","","",""], 20, deck_incr, ["deck"])
myGui.addList("deck", (660, 410, 160, 200), (250, 250, 250), ["..."], 20, None, ["deck"])





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
		myBoard.draw(myDisplay, highlights_white = highlights_white, highlights_red = highlights_red)
		myGui.draw()
		pygame.display.update()

pygame.quit()
quit()