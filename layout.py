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


	def getScreenState(self,dimX:int,dimY:int) -> list[list[int]]:
		# Create a character representation intended to print to the screen
		if dimX != self.dimX or dimY != self.dimY:
			self.screenState = [[(32,'')] * dimY for _ in range(dimX)]
			self.dimX = dimX
			self.dimY = dimY
		else:
			# Revert screen matrix to blank
			for col in self.screenState:
				for cellIndex in range(0,len(col)):
					col[cellIndex] = (32,'')

		# draw deck
		if self.cursorY == 0 and self.cursorX == 0:
			color = Fore.GREEN
		elif self.selectionCoordinates[1] == 0 and self.selectionCoordinates[0] == 0:
			color = Fore.BLUE
		else:
			color = Fore.WHITE
		if len(self.deck.cards) > 0:
			self.putCardBox(0, 0, '#', color)
			if len(self.deck.cards) > 1:
				self.putCardBox(0, 1, '#', color)
				if len(self.deck.cards) > 2:
					self.putCardBox(0, 2, '#', color)
		else:
			self.putCardBox(0, 0, color = color)

		# draw upDeck
		if self.cursorY == 0 and self.cursorX == 1:
			color = Fore.GREEN
		elif self.selectionCoordinates[1] == 0 and self.selectionCoordinates[0] == 1:
			color = Fore.BLUE
		else:
			color = Fore.WHITE
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
			if self.cursorY == 0 and self.cursorX == pileIndex + 3:
				color = Fore.GREEN
			elif self.selectionCoordinates[1] == 0 and self.selectionCoordinates[0] == pileIndex + 3:
				color = Fore.BLUE
			else:
				color = Fore.WHITE
			self.drawPile(30+9*pileIndex,0,self.acePiles[pileIndex], splay = False, color = color)

		# draw cardStacks
		for pileIndex in range(0,len(self.cardStacks)):
			if self.cursorY == 1 and self.cursorX == pileIndex:
				color = Fore.GREEN
			elif self.selectionCoordinates[1] == 1 and self.selectionCoordinates[0] == pileIndex:
				color = Fore.BLUE
			else:
				color = Fore.WHITE
			self.drawPile(pileIndex * 10,13,self.cardStacks[pileIndex], color = color)

		# draw message
		self.putString(self.message,70,2)
		self.putString('x: '+str(self.cursorX),70,4)
		self.putString('y: '+str(self.cursorY), 70, 5)
		self.putString('suby: '+str(self.cursorSubY), 70, 6)
		self.putString('max: '+str(self.cursorSubMax), 70, 7)
		self.putString('sel: '+str(self.selectionCoordinates),70,8)
		self.putString('depth: '+str(self.selectionDepth),70,9)
		if self.selectionCard is None:
			self.putString('card: None', 70, 10)
		else:
			self.putString('card: '+str(self.selectionCard.getIndex())+' '+cardNumToChar(self.selectionCard.getNumber())+symbolFromSuit(self.selectionCard.getSuit()),70,10)

		return self.screenState


	def drawPile(self,x:int,y:int,pile:CardStack,splay:bool = True, color = Fore.WHITE):
		if len(pile.cards) > 0:
			if splay:
				for thisCard in pile.cards:
					if thisCard.faceDown:
						# Each card that is face down beneath other cards is represented by one row of characters
						self.putCardBox(x, y)
						y += 1
					else:
						self.putCard(thisCard, x, y, color = color)
						y += 3
			else:
				self.putCard(pile.cards[-1], x, y)
		else:
			self.putCardBox(x, y, color = color)

	def putCard(self,card:Card,x:int,y:int, color = Fore.WHITE):
		# Places the characters representing the given card at top left position x,y
		self.putCardBox(x, y, color = color)
		self.putCardSymbols(x, y, symbolFromSuit(card.getSuit()), card.getNumber(),card.getColor())
		pass


	def putCardBox(self,x:int,y:int,emptySymbol:str = ' ', color=Fore.WHITE):
		# Places the line around a card at a given top left position x,y
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
		# Places the character at the position x,y
		if len(self.screenState) > x and len(self.screenState[x]) > y and len(character) == 1:
			self.screenState[x][y] = (ord(character),color)
			return True
		else:
			return False


	def putString(self,instr:str,x,y,color:str=Fore.WHITE):
		# Writes text at the position x,y
		currentX = x
		currentY = y
		for character in instr:
			self.putChar(character,currentX,currentY,color)
			currentX += 1
			if currentX >= self.dimX:
				currentX = x
				currentY += 1


	def moveRight(self):
		if self.cursorX < 6:
			self.cursorX += 1
			if self.cursorY == 0:
				if self.cursorX == 2:
					self.cursorX += 1
			else:
				self.setCursorSubY()


	def moveLeft(self):
		if self.cursorX > 0:
			self.cursorX -= 1
			if self.cursorY == 0:
				if self.cursorX == 2:
					self.cursorX -= 1
			else:
				self.setCursorSubY()


	def moveUp(self):
		if self.cursorY > 0:
			if self.cursorSubY > 0:
				self.cursorSubY -= 1
			else:
				self.cursorY -= 1
		if self.cursorX == 2:
			self.cursorX = 1


	def moveDown(self):
		if self.cursorY == 0:
			self.cursorY += 1
			self.setCursorSubY()
		elif self.cursorSubY < self.cursorSubMax:
			self.cursorSubY += 1


	def spaceAction(self):
		if self.selectionCoordinates[0] == -1:
			self.makeSelection()
		elif self.cursorX == self.selectionCoordinates[0] and self.cursorY == self.selectionCoordinates[1]:
			self.removeSelection()
		else:
			self.applySelection()


	def makeSelection(self):
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
		try:
			self.selectionCoordinates = (self.cursorX, self.cursorY, self.cursorSubY)
			self.selectionCard = self.selectionSourceStack.cards[-self.selectionDepth]
		except:
			print(self.selectionDepth)
			raise Exception("A")
		return True


	def applySelection(self) -> bool:
		if self.selectionCard is None:
			self.message = "No card currently selected."
			return False
		if self.cursorY == 0:
			if self.cursorX <= 2:
				self.message = "Cannot place a card on the draw deck."
				return False
			else:
				# Attepting to place a card on an ace pile.
				if self.selectionDepth != 1:
					self.message = "Cannot place multiple cards on an ace pile."
					return False
				if self.selectionCard.getSuit() != suitFromNumber(self.cursorX - 2):
					self.message = "Suit does not match ace pile suit."
					return False
				targetCardstack = self.acePiles[self.cursorX - 2]
				if len(targetCardstack.cards) == 0:
					if self.selectionCard.getNumber() != 1:
						self.message = "Must start with an ace."
						return False
				else:
					if self.selectionCard.getNumber() != targetCardstack.cards[-1].getNumber() + 1:
						self.message = "Card number is not correct."
						return False
		else:
			# Attempting to place a card on another card stack.
			targetCardstack = self.cardStacks[self.cursorX]
			if len(targetCardstack.cards) > 0:
				denominatorCard = targetCardstack.cards[-1]
				if denominatorCard.getColor() == self.selectionCard.getColor():
					self.message = "Color mismatch. "+str(denominatorCard.getColor()) + str(self.selectionCard.getColor())
					return False
				if denominatorCard.getNumber() - 1 != self.selectionCard.getNumber():
					self.message = "Card number is not correct. (2) "+ str(denominatorCard.getNumber()) + ','+str(self.selectionCard.getNumber())
					return False
		# If the function has not retunred above, assume that applying the selection is valid:

		poppedCards = self.selectionSourceStack.popX(self.selectionDepth)
		targetCardstack.addCards(poppedCards)
		self.removeSelection()
		return True


	def removeSelection(self):
		self.selectionCoordinates = (-1, -1, -1)
		self.selectionSourceStack = None
		self.selectionDepth = 0
		self.selectionCard = None


	def setCursorSubY(self):
		self.cursorSubMax = self.cardStacks[self.cursorX].getUpCardCount() - 1
		self.cursorSubY = self.cursorSubMax