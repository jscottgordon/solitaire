#!/usr/bin/env python3

import os
import random
import math

def main():
	# Initialize deck of cards in order, then randomly shuffle
	deckList = [None] * 52
	for i in range(0,52):
		deckList[i] = Card(i)
	random.shuffle(deckList)

	deck = CardStack(deckList)

	# Deal cards into seven piles
	cardStacks = [None] * 7
	for i in range(0,7):
		cardStacks[i] = CardStack(deckList.popX(i+1))
		cardStacks[i][0].flipUp()

def refreshScreen():
	os.system('cls||clear')

class Card:
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
	def __init__(self, cardList = None):
		# cardList is an optional initialization of the card stack
		if cardList is None:
			self.cards = []
		else
			self.cards = cardList
	def popX(self,x) -> list[Card]:
		# Remove X cards from the stack, and return those X
		poppedCards = self.cards[:n]
		self.cards = self.cards[n:]
		return poppedCards


class AcePile(cardStack):
	def __init__(self):

class MainPile(cardStack):
	def __init__(self):

class TurnPile(cardStack):
	def __init__(self):

def suitFromNumber(suitNumber) -> str:
	if suitNumber == 0:
		return 'spades'
	elif suitNumber == 1:
		return 'diamonds'
	elif suitNumber == 2:
		return 'clubs'
	elif suitNumber == 3:
		return 'hearts'
	else:
		return None

if __name__ == "__main__":
   main()