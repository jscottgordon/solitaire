#!/usr/bin/env python3

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

class CardStack:
	"""General class for any stack of cards"""

	def __init__(self, cardList:list[Card] = None):
		# cardList is an optional initialization of the card stack
		if cardList is None:
			self.cards = []
		else
			self.cards = cardList
	def popX(self,x) -> list[Card]:
		# Remove X cards from the stack, and return those X
		poppedCards = self.cards[:n]
		TODO(make sure the cards are popped in the correct order)
		self.cards = self.cards[n:]
		return poppedCards
	def addCard(self,card):
		self.cards.append(card)


class AcePile(cardStack):
	"""Class for the ace piles at the top of the board"""

	def __init__(self):
		super().__init__()
	def addCard(self,card):
		super().addCard(card)
		self.cards[-1].flipUp()


class TurnPile(cardStack):
	def __init__(self):