#!/usr/bin/env python3

def suitFromNumber(suitNumber: int) -> str:
    if suitNumber == 0:
        return 'spades'
    elif suitNumber == 1:
        return 'diamonds'
    elif suitNumber == 2:
        return 'clubs'
    elif suitNumber == 3:
        return 'hearts'
    else:
        return ''


def symbolFromSuit(suit: str) -> str:
    if suit == 'spades':
        return chr(9824)
    elif suit == 'diamonds':
        return chr(9830)
    elif suit == 'clubs':
        return chr(9827)
    elif suit == 'hearts':
        return chr(9829)
    else:
        return chr(32)


def cardNumToChar(num:int) -> str:
    if num == 1:
        return 'A'
    elif num == 11:
        return 'J'
    elif num == 12:
        return 'Q'
    elif num == 13:
        return 'K'
    elif num == 10:
        return 'X'
    else:
        return str(num)