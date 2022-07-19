#!/usr/bin/env python3

from utils import *
import math


class Card:
	"""Represents a specific card"""

	def __init__(self,cardIndex:int):
		self.cardIndex = cardIndex
		self.faceDown = True
		# The order of cards is:
		# 13 Spades, 13 Diamonds, 13 Clubs, 13 Hearts.
		# Each suit is ordered Ace to King.

	def getIndex(self) -> int:
		return self.cardIndex

	def getSuit(self) -> str:
		return suitFromNumber(math.floor(self.cardIndex / 13))

	def getNumber(self) -> int:
		return self.cardIndex + 1 - 13 * (math.floor(self.cardIndex / 13))

	def flip(self):
		self.faceDown = not self.faceDown

	def flipUp(self):
		self.faceDown = False

	def flipDown(self):
		self.faceDown = True

	def getColor(self):
		suit = self.getSuit()
		if suit == 'spades' or suit == 'clubs':
			return 'black'
		else:
			return 'red'


class CardStack:
	"""General class for any stack of cards"""

	def __init__(self, cardList:list[Card] = None):
		# cardList is an optional initialization of the card stack
		if cardList is None:
			self.cards = []
		else:
			self.cards = cardList

	def popX(self,x) -> list[Card]:
		# Remove X cards from the stack, and return those X
		poppedCards = self.cards[x-1:]
		poppedCards.reverse()
		self.cards = self.cards[:x-1]
		return poppedCards

	def addCard(self,newCard:Card):
		# Add a card to the stack
		if self.checkValidCardPlacement(newCard):
			self.cards.append(newCard)
			return True
		else:
			return False

	def addCards(self,newCards:list[Card]):
		if self.checkValidCardPlacement(newCards[0]):
			self.cards += newCards
			return True
		else:
			return False

	def checkValidCardPlacement(self,card:Card):
		return True


class AcePile(CardStack):
	"""Class for the ace piles at the top of the board"""

	def __init__(self,suit:str):
		self.cardList = None
		self.suit = suit
		super().__init__()

	def checkValidCardPlacement(self,card:Card):
		if card.getSuit() != self.suit:
			return False
		if self.cardList.len() == 0:
			if card.getNumber() == 0:
				return True
			else:
				return False
		else:
			# There is at least one card already in this AcePile
			if card.getNumber == self.cardList[-1].getNumber() + 1:
				return True
			else:
				return False
		return False


class PlayStack(CardStack):
	"""Represents one of the seven piles at the bottom of the board"""

	def __init__(self, startingCards: list[Card]):
		self.cardList = None
		for card in startingCards:
			card.flipDown()
		startingCards[-1].flipUp()
		super().__init__(startingCards)

	def checkValidCardPlacement(self,card:Card):
		if self.cardList.len() == 0:
			return True
		else:
			# There is at least one card already in this CardStack
			if self.cardList[-1].getColor() == card.getColor():
				return False
			else:
				if self.cardList[-1].getNumber() - 1 == card.getNumber():
					return True
				else:
					return False
		return False

	def popX(self,x):
		super().popX(x)
		if self.cardList.len() > 0:
			self.cardList[-1].flipUp()