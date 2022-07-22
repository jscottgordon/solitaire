#!/usr/bin/env python3

import os
import sys
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
    refreshScreen()
    with keyboard.Listener(on_press=keyPress, on_release=keyRelease) as listener:
        listener.join()

def refreshScreen():
    """Reprint the screen, fill the whole terminal window with characters from a 2D array from getScreenState"""

    if sys.platform == "win32" and os.environ.get("WT_SESSION"):
        os.system('cls')
    else:
        os.system('clear')
    tsize = os.get_terminal_size()
    outchars = gameLayout.getScreenState(tsize.columns, tsize.lines - 1)
    for y in range(0, len(outchars[0])):
        for x in range(0,len(outchars)):
            print(outchars[x][y][1]+chr(outchars[x][y][0]), end='')  # [1] represents the color, [0] is the character
        print('\n', end='')

def keyPress(key):
    """Used to detect relevant keyboard key presses and pass them down into the gameLayout"""

    if key == keyboard.Key.right:
        gameLayout.moveRight()
    elif key == keyboard.Key.left:
        gameLayout.moveLeft()
    elif key == keyboard.Key.up:
        gameLayout.moveUp()
    elif key == keyboard.Key.down:
        gameLayout.moveDown()
    elif key == keyboard.Key.space:
        gameLayout.spaceAction()
    elif key == keyboard.Key.esc:
        gameLayout.removeSelection()
    refreshScreen()
    if gameLayout.winState:
        print("Game won!")
        return False

def keyRelease(key):
    """Used for detecting the quit key: Q"""

    if isinstance(key, keyboard.KeyCode) and key.char == 'q':
        return False


if __name__ == "__main__":
    main()
