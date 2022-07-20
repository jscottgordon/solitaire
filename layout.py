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
			self.cardStacks[i] = PlayStack(self.deck.popX(i + 1))
			#self.cardStacks[i].flipTop()
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

		# draw upDeck

		# draw acePiles

		# draw cardStacks

		return self.screenState


	def putCard(self,card:Card,x:int,y:int):
		# Places the characters representing the given card at top left position x,y
		self.putCardBox(x, y)
		self.putCardSymbols(x, y, symbolFromSuit(card.getSuit()), card.getNumber(),card.getColor())
		pass


	def putCardBox(self,x:int,y:int,emptySymbol:str = ' '):
		# Places the line around a card at a given top left position x,y
		self.putChar(chr(9484), x, y)  # Top left corner
		self.putChar(chr(9492), x, y + 8)  # Bottom left corner
		self.putChar(chr(9488), x + 8, y)  # Top right corner
		self.putChar(chr(9496), x + 8, y + 8)  # Bottom right corner
		for i in range(x + 1, x + 8):
			# Draw top and bottom lines
			self.putChar(chr(9472), i, y)
			self.putChar(chr(9472), i, y + 8)
		for i in range(y + 1, y + 8):
			# Draw left and right lines
			self.putChar(chr(9474), x, i)
			self.putChar(chr(9474), x + 8, i)
			for j in range(x + 1, x + 8):
				self.putChar(emptySymbol, j, i)


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