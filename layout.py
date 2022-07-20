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

		# Deal cards into seven piles
		self.cardStacks = [None] * 7
		for i in range(0,7):
			poppedCards = self.deck.popX(i + 1)
			print('poppedCards',len(poppedCards))
			self.cardStacks[i] = PlayStack(poppedCards)
			# self.cardStacks[i].flipTop()
			print(len(self.cardStacks[i].cards))

		# Initialize the ace piles
		self.acePiles = [None] * 4
		for i in range(0,4):
			self.acePiles[i] = AcePile(suitFromNumber(i))


	def getScreenState(self,dimX:int,dimY:int) -> list[list[int]]:
		# Create a character representation intended to print to the screen
		if dimX != self.dimX or dimY != self.dimY:
			self.screenState = [[(32,'')] * dimY for i in range(dimX)]

		# draw deck
		if len(self.deck.cards) > 0:
			self.putCardBox(0, 0, '#')
			if len(self.deck.cards) > 1:
				self.putCardBox(0, 1, '#')
				if len(self.deck.cards) > 2:
					self.putCardBox(0, 2, '#')
		else:
			self.putCardBox(0, 0)

		# draw upDeck
		if len(self.upDeck.cards) > 2:
			self.putCard(self.upDeck.cards[0], 11, 0)
			self.putCard(self.upDeck.cards[1], 13, 2)
			self.putCard(self.upDeck.cards[2], 15, 4)
		elif len(self.upDeck.cards) > 1:
			self.putCard(self.upDeck.cards[0], 11, 0)
			self.putCard(self.upDeck.cards[1], 13, 2)
		elif len(self.upDeck.cards) > 0:
			self.putCard(self.upDeck.cards[0], 11, 0)
		else:
			self.putCardBox(11, 0)

		# draw acePiles
		for pileIndex in range(0,len(self.acePiles)):
			self.drawPile(30+9*pileIndex,0,self.acePiles[pileIndex])

		# draw cardStacks
		for pileIndex in range(0,len(self.cardStacks)):
			self.drawPile(pileIndex * 10,13,self.cardStacks[pileIndex])

		return self.screenState


	def drawPile(self,x:int,y:int,pile:CardStack):
		if len(pile.cards) > 0:
			for thisCard in pile.cards:
				if thisCard.faceDown:
					# Each card that is face down beneath other cards is represented by one row of characters
					self.putCardBox(x, y)
					y += 1
				else:
					self.putCard(thisCard, x, y)
					y += 3
		else:
			self.putCardBox(x, y)

	def putCard(self,card:Card,x:int,y:int):
		# Places the characters representing the given card at top left position x,y
		self.putCardBox(x, y)
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

	def putChar(self,character,x:int,y:int,color:str=Fore.WHITE):
		# Places the character at the position x,y
		if len(self.screenState) > x and len(self.screenState[x]) > y:
			self.screenState[x][y] = (ord(character),color)
			return True
		else:
			return False