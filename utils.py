#!/usr/bin/env python3

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
        return ''