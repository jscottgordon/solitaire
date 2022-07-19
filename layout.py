#!/usr/bin/env python3

import card

class Layout():
	"""Represents a solitaire game layout"""

	def __init__(self,deckList):
		# Deck represents the remaining cards that don't get dealt into piles
		self.deck = CardStack(deckList)

		# Deal cards into seven piles
		self.cardStacks = [None] * 7
		for i in range(0,7):
			cardStacks[i] = CardStack(deckList.popX(i + 1))
			cardStacks[i][0].flipUp()

		# Initialize the ace piles

		self.acePiles = [None] * 4
		for i in range(0,4):
			acePiles = AcePile()