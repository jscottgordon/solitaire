#!/usr/bin/env python3

from card import Card, CardStack, AcePile, PlayStack
from utils import *
from colorama import Fore, Style


class SolitaireLayout:
	"""Represents a solitaire game layout"""

	def __init__(self,deckList):
		# Deck represents the remaining cards that don't get dealt into piles
		self.deck = CardStack(deckList)
		self.upDeck = CardStack()
		self.screenState = [[]]
		self.dimX = -1
		self.dimY = -1
		self.cursorX = 0
		self.cursorY = 0
		self.cursorSubY = 0
		self.cursorSubMax = 0
		self.selectionCoordinates = (-1, -1, -1)
		self.selectionSourceStack = None
		self.selectionDepth = 0
		self.selectionCard = None
		self.message = "Use the arrow keys to move your selection, space to select, and escape to exit selection.  Press Q to exit."
		self.winState = False

		# Deal cards into seven piles
		self.cardStacks = [None] * 7
		for i in range(0,7):
			poppedCards = self.deck.popX(i + 1)
			self.cardStacks[i] = PlayStack(poppedCards)
			self.cardStacks[i].flipTop()

		# Initialize the ace piles
		self.acePiles = [None] * 4
		for i in range(0,4):
			self.acePiles[i] = AcePile(suitFromNumber(i))


	def getScreenState(self, dimX:int, dimY:int) -> list[list[int]]:
		"""Generates a 2D array of characters representing the desired terminal screen"""

		# Create a character representation intended to print to the screen
		# self.screenState should be an array of arrays,
		# where each component of the inner array is tuple (charCode: int, color: str)
		if dimX != self.dimX or dimY != self.dimY:
			# If the terminal window is resized, regenerate the screenState array based on the new dimensions
			self.screenState = [[(32, '')] * dimY for _ in range(dimX)]
			self.dimX = dimX
			self.dimY = dimY
		else:
			# We know the terminal was not resized, so revert the existing matrix to blank spaces
			for col in self.screenState:
				for cellIndex in range(0, len(col)):
					col[cellIndex] = (32, '')

		# Now, draw all components of the solitaire screen:

		# First, draw the deck in the top left corner
		color = determineSelectionColor(0, 0)
		if len(self.deck.cards) > 0:
			self.putCardBox(0, 0, '#', color)
			if len(self.deck.cards) > 1:
				self.putCardBox(0, 1, '#', color)
				if len(self.deck.cards) > 2:
					self.putCardBox(0, 2, '#', color)
		else:
			self.putCardBox(0, 0, color = color)

		# draw upDeck
		color = determineSelectionColor(1, 0)
		if len(self.upDeck.cards) > 2:
			self.putCard(self.upDeck.cards[-3], 11, 0)
			self.putCard(self.upDeck.cards[-2], 13, 2)
			self.putCard(self.upDeck.cards[-1], 15, 4, color)
		elif len(self.upDeck.cards) > 1:
			self.putCard(self.upDeck.cards[-2], 11, 0)
			self.putCard(self.upDeck.cards[-1], 13, 2, color)
		elif len(self.upDeck.cards) > 0:
			self.putCard(self.upDeck.cards[0], 11, 0, color)
		else:
			self.putCardBox(11, 0, color = color)

		# draw acePiles
		for pileIndex in range(0,len(self.acePiles)):
			color = determineSelectionColor(pileIndex + 3, 0)
			self.drawPile(30+9*pileIndex,0,self.acePiles[pileIndex], splay = False, color = color)
			if len(self.acePiles[pileIndex].cards) == 0:
				self.putChar(symbolFromSuit(suitFromNumber(pileIndex)), 34+9*pileIndex, 4, color = color)

		# draw cardStacks
		for pileIndex in range(0,len(self.cardStacks)):
			color = determineSelectionColor(pileIndex, 0)
			self.drawPile(pileIndex * 10, 13, self.cardStacks[pileIndex], color = color, colorDepth = self.cursorSubY)

		# draw message
		self.putString(self.message, 70, 2)

		return self.screenState

	def determineSelectionColor(self,x:int,y:int):
		"""Figure out if the cursor or selection is pointing to the location (x,y),
		and return the appropriate highlight color"""
		if self.cursorX == x and self.cursorY == y:
			return Fore.GREEN
		elif self.selectionCoordinates[0] == x and self.selectionCoordinates[1] == y:
			return Fore.BLUE
		else:
			return Fore.WHITE


	def drawPile(self,x:int, y:int, pile:CardStack, splay:bool = True, color = Fore.WHITE, colorDepth = 1):
		"""Draw the cards on the screen at (x,y) from the passed CardStack object."""
		if len(pile.cards) > 0:
			if splay:
				faceUpCardCount = 0
				for thisCard in pile.cards:
					if thisCard.faceDown:
						# Each card that is face down beneath other cards is represented by one row of characters
						self.putCardBox(x, y)
						y += 1
					else:
						if faceUpCardCount >= colorDepth:
							colorToPass = color
						else:
							colorToPass = Fore.WHITE
						self.putCard(thisCard, x, y, color = colorToPass)
						y += 3
						faceUpCardCount += 1
			else:
				self.putCard(pile.cards[-1], x, y, color = color)
		else:
			self.putCardBox(x, y, color = color)

	def putCard(self,card:Card,x:int,y:int, color = Fore.WHITE):
		"""Places the characters representing the given card at top left position x,y"""
		self.putCardBox(x, y, color = color)
		self.putCardSymbols(x, y, symbolFromSuit(card.getSuit()), card.getNumber(),card.getColor())
		pass


	def putCardBox(self,x:int,y:int,emptySymbol:str = ' ', color=Fore.WHITE):
		"""Places a border line around a card at a given top left position x,y"""
		self.putChar(chr(9484), x, y, color)  # Top left corner
		self.putChar(chr(9492), x, y + 8, color)  # Bottom left corner
		self.putChar(chr(9488), x + 8, y, color)  # Top right corner
		self.putChar(chr(9496), x + 8, y + 8, color)  # Bottom right corner
		for i in range(x + 1, x + 8):
			# Draw top and bottom lines
			self.putChar(chr(9472), i, y, color)
			self.putChar(chr(9472), i, y + 8, color)
		for i in range(y + 1, y + 8):
			# Draw left and right lines
			self.putChar(chr(9474), x, i, color)
			self.putChar(chr(9474), x + 8, i, color)
			for j in range(x + 1, x + 8):
				self.putChar(emptySymbol, j, i, color)


	def putCardSymbols(self,x:int,y:int,symbol:str,num:int,color=Fore.WHITE):
		"""Draws the suit symbols on a card, where the location of the symbols depends on the card number"""
		numberSymbol = cardNumToChar(num)
		# First, draw upper and lower corner card symbols
		if num==10:
			self.putChar('1', x + 1, y + 1, color)
			self.putChar('0', x + 7, y + 7, color)
			self.putChar('0', x + 2, y + 1, color)
			self.putChar('1', x + 6, y + 7, color)
		else:
			self.putChar(numberSymbol, x + 1, y + 1, color)
			self.putChar(numberSymbol, x + 7, y + 7, color)
		self.putChar(symbol, x + 1, y + 2, color)
		self.putChar(symbol, x + 7, y + 6, color)

		# Then, draw card art that depends on the number
		if num == 1 or num == 3 or num == 5:
			self.putChar(symbol, x + 4, y + 4, color)
		if num == 2 or num == 3 or num == 8:
			self.putChar(symbol, x + 4, y + 3, color)
			self.putChar(symbol, x + 4, y + 5, color)
		if num == 4 or num == 5 or num == 9 or num == 10:
			self.putChar(symbol, x + 3, y + 3, color)
			self.putChar(symbol, x + 3, y + 5, color)
			self.putChar(symbol, x + 5, y + 3, color)
			self.putChar(symbol, x + 5, y + 5, color)
		if num == 6 or num == 7 or num == 8:
			self.putChar(symbol, x + 3, y + 2, color)
			self.putChar(symbol, x + 3, y + 4, color)
			self.putChar(symbol, x + 3, y + 6, color)
			self.putChar(symbol, x + 5, y + 2, color)
			self.putChar(symbol, x + 5, y + 4, color)
			self.putChar(symbol, x + 5, y + 6, color)
		if num == 7:
			self.putChar(symbol, x + 4, y + 3, color)
		if num == 9 or num == 10:
			self.putChar(symbol, x + 3, y + 1, color)
			self.putChar(symbol, x + 3, y + 7, color)
			self.putChar(symbol, x + 5, y + 1, color)
			self.putChar(symbol, x + 5, y + 7, color)
		if num == 10:
			self.putChar(symbol, x + 4, y + 2, color)
		if num == 11:
			self.putChar(chr(9813), x + 4, y + 4, Fore.YELLOW)
		if num == 12:
			self.putChar(chr(9812),x + 4, y + 4, Fore.YELLOW)
		if num == 13:
			self.putChar(chr(9815),x + 4, y + 4, Fore.YELLOW)


	def putChar(self,character:str,x:int,y:int,color:str=Fore.WHITE):
		"""Draw the character at the position x,y"""
		if len(self.screenState) > x and len(self.screenState[x]) > y and len(character) == 1:
			self.screenState[x][y] = (ord(character),color)
			return True
		else:
			return False


	def putString(self,instr:str,x,y,color:str=Fore.WHITE):
		"""Writes text at the position x,y on the screen"""
		currentX = x
		currentY = y
		for character in instr:
			self.putChar(character,currentX,currentY,color)
			currentX += 1
			if currentX >= self.dimX:
				currentX = x
				currentY += 1


	def moveRight(self):
		"""Moves the cursor right"""
		if self.cursorX < 6:
			self.cursorX += 1
			if self.cursorY == 0:
				if self.cursorX == 2:
					self.cursorX += 1
			else:
				self.setCursorSubY()


	def moveLeft(self):
		"""Moves the cursor left"""
		if self.cursorX > 0:
			self.cursorX -= 1
			if self.cursorY == 0:
				if self.cursorX == 2:
					self.cursorX -= 1
			else:
				self.setCursorSubY()


	def moveUp(self):
		"""Moves the cursor up"""
		if self.cursorY > 0:
			if self.cursorSubY > 0:
				self.cursorSubY -= 1
			else:
				self.cursorY -= 1
		if self.cursorX == 2:
			self.cursorX = 1


	def moveDown(self):
		"""Moves the cursor down"""
		if self.cursorY == 0:
			self.cursorY += 1
			self.setCursorSubY()
		elif self.cursorSubY < self.cursorSubMax:
			self.cursorSubY += 1


	def spaceAction(self):
		"""Makes or applies selection, depending on cursor position"""
		if self.selectionCoordinates[0] == -1:
			self.makeSelection()
		elif self.cursorX == self.selectionCoordinates[0] and self.cursorY == self.selectionCoordinates[1]:
			self.removeSelection()
		else:
			self.applySelection()


	def makeSelection(self):
		"""Selects the current card, or flips the deck if the deck is targeted"""
		if self.cursorY == 0:
			if self.cursorX == 0:
				# Flip deck over
				if len(self.deck.cards) == 0:
					self.deck.addCards(self.upDeck.popX(len(self.upDeck.cards)))
					for aCard in self.deck.cards:
						aCard.flipDown()
				else:
					poppedCards = self.deck.popX(3)
					for aCard in poppedCards:
						aCard.flipUp()
					self.upDeck.addCards(poppedCards)
				self.removeSelection()
				return False
			elif self.cursorX == 1:
				# Face up deck cards
				self.selectionSourceStack = self.upDeck
				self.selectionDepth = 1
			else:
				self.selectionSourceStack = self.acePiles[self.cursorX-3]
				self.selectionDepth = 1
		else:
			self.selectionSourceStack = self.cardStacks[self.cursorX]
			self.selectionDepth = self.selectionSourceStack.getUpCardCount() - self.cursorSubY
		if len(self.selectionSourceStack.cards) == 0:
			self.removeSelection()
			return False
		self.selectionCoordinates = (self.cursorX, self.cursorY, self.cursorSubY)
		self.selectionCard = self.selectionSourceStack.cards[-self.selectionDepth]
		return True


	def applySelection(self) -> bool:
		"""Attemps to move cards based on the current selection to the current cursor position"""
		checkForWin = False
		if self.selectionCard is None:
			return False
		if self.cursorY == 0:
			if self.cursorX <= 2:
				return False
			else:
				# Attepting to place a card on an ace pile.
				if self.selectionDepth != 1:
					return False
				if self.selectionCard.getSuit() != suitFromNumber(self.cursorX - 3):
					return False
				targetCardstack = self.acePiles[self.cursorX - 3]
				checkForWin = True
		else:
			# Attempting to place a card on another card stack.
			targetCardstack = self.cardStacks[self.cursorX]
		if not targetCardstack.checkValidCardPlacement(self.selectionCard):
			return False
		# If the function has not retunred above, assume that applying the selection is valid:

		poppedCards = self.selectionSourceStack.popX(self.selectionDepth, invert = False)
		print(poppedCards)
		print(targetCardstack.addCards(poppedCards))
		print(str(len(targetCardstack.cards)))
		self.removeSelection()
		if checkForWin:
			self.getWinState()
		return True


	def getWinState(self):
		"""Checks to see if the game is currently won"""
		for acePile in self.acePiles:
			if len(acePile.cards) != 13:
				return False
		self.winState = True
		return True


	def removeSelection(self):
		"""Resets the current selection"""
		self.selectionCoordinates = (-1, -1, -1)
		self.selectionSourceStack = None
		self.selectionDepth = 0
		self.selectionCard = None


	def setCursorSubY(self):
		"""Used for moving the cursor up or down the card stack"""
		self.cursorSubMax = self.cardStacks[self.cursorX].getUpCardCount() - 1
		self.cursorSubY = self.cursorSubMax