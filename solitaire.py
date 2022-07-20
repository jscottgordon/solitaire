#!/usr/bin/env python3

import os
import random
import math
from pynput import keyboard

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
    gameLayout.message = "Use the arrow keys to move your selection, space to select, and escape to exit selection.  Press Esc to exit."
    refreshScreen()
    with keyboard.Listener(on_press=keyPress, on_release=keyRelease) as listener:
        listener.join()

def refreshScreen():
    os.system('cls||clear')
    tsize = os.get_terminal_size()
    outchars = gameLayout.getScreenState(tsize.columns, tsize.lines - 1)
    for y in range(0, len(outchars[0])):
        for x in range(0,len(outchars)):
            print(outchars[x][y][1]+chr(outchars[x][y][0]),end='')  # [1] represents the color, [0] is the character
        print('\n',end='')

def keyPress(key):
    if key == keyboard.Key.right:
        gameLayout.rightPressed()
    elif key == keyboard.Key.left:
        gameLayout.leftPressed()
    elif key == keyboard.Key.up:
        gameLayout.upPressed()
    elif key == keyboard.Key.down:
        gameLayout.downPressed()
    refreshScreen()

def keyRelease(key):
    if key == keyboard.Key.esc:
        return False


if __name__ == "__main__":
    main()
