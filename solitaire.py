#!/usr/bin/env python3

import os
import random
import math

from layout import Layout
from card import Card

global gameLayout


def main():
    # Initialize deck of cards in order, then randomly shuffle
    deckList = [None] * 52
    for i in range(0, 52):
        deckList[i] = Card(i)
    random.shuffle(deckList)

    # Set up new Solitaire game layout
    Layout(deckList)


def refreshScreen():
    os.system('cls||clear')





if __name__ == "__main__":
    main()
