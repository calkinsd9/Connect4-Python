#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Play a game of Connect 4 (or more)')

parser.add_argument('-w', '--width', default=7, type=int, help='an integer that sets the width of the board', metavar='int')
parser.add_argument('-he', '--height', default=7, type=int, help='an integer that sets the height of the board', metavar='int')
parser.add_argument('-c', '--connect', default=4, type=int, help='an integer that sets the number of spaces needed to win', metavar='int')
parser.add_argument('-s', '--square', type=int, help='an integer that sets the width and height of a square board', metavar='int')
parser.add_argument('-l', '--load', type=str, help='a filename with a save game object to be loaded', metavar='filename')

args = parser.parse_args()
print (vars(args))
