#!/usr/bin/env python3

import os
import random
import math

import layout
import card

global gameLayout
def main():
	# Initialize deck of cards in order, then randomly shuffle
	deckList = [None] * 52
	for i in range(0,52):
		deckList[i] = Card(i)
	random.shuffle(deckList)

	# Set up new Solitaire game layout
	Layout(deckList)



def refreshScreen():
	os.system('cls||clear')


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