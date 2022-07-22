#!/usr/bin/env python3

from utils import *
import math
from colorama import Fore


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
			return Fore.WHITE
		else:
			return Fore.RED


class CardStack:
	"""General class for any stack of cards"""

	def __init__(self, cardList:list[Card] = None):
		# cardList is an optional initialization of the card stack
		if cardList is None:
			self.cards = []
		else:
			self.cards = cardList

	def popX(self,x: int, invert: bool = True) -> list[Card]:
		# Remove X cards from the stack, and return those X
		poppedCards = self.cards[len(self.cards) - x:]
		if invert:
			poppedCards.reverse()
		self.cards = self.cards[:len(self.cards) - x]
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

	def getUpCardCount(self) -> int:
		faceUpSum = 0
		for aCard in self.cards:
			if not aCard.faceDown:
				faceUpSum += 1
		return faceUpSum


class AcePile(CardStack):
	"""Class for the ace piles at the top of the board"""

	def __init__(self,suit:str):
		self.cards = None
		self.suit = suit
		super().__init__()

	def checkValidCardPlacement(self,card:Card):
		if card.getSuit() != self.suit:
			print(card.getSuit(),self.suit)
			return False
		if len(self.cards) == 0:
			if card.getNumber() == 1:
				return True
			else:
				print(card.getNumber(), 1)
				return False
		else:
			# There is at least one card already in this AcePile
			if card.getNumber() == self.cards[-1].getNumber() + 1:
				return True
			else:
				print(card.getNumber(), self.cards[-1].getNumber() + 1)
				return False


class PlayStack(CardStack):
	"""Represents one of the seven piles at the bottom of the board"""

	def __init__(self, startingCards: list[Card]):
		self.cards = None
		for card in startingCards:
			card.flipDown()
		super().__init__(startingCards)
		self.flipTop()

	def checkValidCardPlacement(self,card:Card):
		if len(self.cards) == 0:
			return True
		else:
			# There is at least one card already in this CardStack
			if self.cards[-1].getColor() == card.getColor():
				return False
			else:
				if self.cards[-1].getNumber() - 1 == card.getNumber():
					return True
				else:
					return False

	def popX(self,x:int, invert: bool = True) -> list[Card]:
		poppedCards = super().popX(x, invert)
		if len(self.cards) > 0:
			self.cards[-1].flipUp()
		return poppedCards

	def flipTop(self):
		# Make sure the top card is face up
		if len(self.cards) > 0:
			print(len(self.cards))
			self.cards[-1].flipUp()