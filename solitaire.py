#!/usr/bin/env python3

import os
import random
import math

from layout import SolitaireLayout
from card import Card

global gameLayout


def main():
    global gameLayout
    # Initialize deck of cards in order, then randomly shuffle
    deckList = [None] * 52
    for i in range(0, 52):
        deckList[i] = Card(i)
    random.shuffle(deckList)

    # Set up new Solitaire game layout
    gameLayout = SolitaireLayout(deckList)
    refreshScreen()
    input('Press enter to exit: ')


def refreshScreen():
    os.system('cls||clear')
    tsize = os.get_terminal_size()
    outchars = gameLayout.getScreenState(tsize.columns, tsize.lines)
    for y in range(0, len(outchars[0])):
        for x in range(0,len(outchars)):
            print(outchars[x][y][1]+chr(outchars[x][y][0]),end='')  # [1] represents the color, [0] is the character
        print('\n',end='')


if __name__ == "__main__":
    main()
