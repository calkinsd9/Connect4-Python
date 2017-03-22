#!/usr/bin/env python

import argparse
import pickle
import os
import sys

#len(gameBoard) == height
#len(gameBoard[0] == width)

EMPTYVAL = '.'
PLAYERVAL = 'x'
COMPVAL = 'o'

def clearScreen():
    #clear screen code taken from  http://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')

def printGameBoard(gameBoard):
    width = len(gameBoard[0])
    height = len(gameBoard)
    padding = 38 - width
    
    print('\n\n')
    print('  _|_|_|                                                      _|      _|  _|')
    print('_|          _|_|    _|_|_|    _|_|_|      _|_|      _|_|_|  _|_|_|_|  _|  _|')
    print('_|        _|    _|  _|    _|  _|    _|  _|_|_|_|  _|          _|      _|_|_|_|')
    print('_|        _|    _|  _|    _|  _|    _|  _|        _|          _|          _|  ')
    print('_|_|_|_|    _|_|    _|    _|  _|    _|    _|_|_|    _|_|_|    _|          _|\n\n')
    
    #add padding to board string
    for i in range(padding):
        boardString += ' '
    
    boardString += '|'
    count = 0
    for row in gameBoard:
        for value in row:
            boardString += value + '|'
            count += 1
            if count == len(gameBoard[0]):
                boardString += '\n|'
                count =0
    boardString = boardString[:-1]
    print(boardString)

def resetGameBoard(gameBoard):
    rowIndex = 0
    for row in gameBoard:
        gameBoard[rowIndex] = list(map(lambda x: EMPTYVAL, row))
        rowIndex += 1
        
        
def validateUserInput(gameBoard, userInput):
    while True:
        if (userInput == 'q' or userInput == 's'):
            return
        
        if (isValidMove(gameBoard, userInput)):
            return
            
        print('Column is full. Please choose another.\n\n')
        userInput = input('\n\nEnter column number where you\'d like to drop your piece\n(Enter \'q\' to quit)\n')
    
    
def isValidMove(gameBoard, userInput):
    iUserInput = int(userInput, 10)
    if (iUserInput > 0 and iUserInput <= len(gameBoard[0])):
        if (gameBoard[iUserInput][0] == EMPTYVAL):
            return True            
    return False
    
def userMove(userInput, gameBoard):
    iUserInput = int(userInput)
    height = len(gameBoard)
    
    for h in range(len(gameBoard)):
        if (gameboard[iUserInput-1][h] != EMPTYVAL):
            break
            
    gameBoard[iUserInput-1][h-1] = PLAYERVAL
    
def checkWin(gameBoard, connect, value):
    width = len(gameBoard[0])
    height = len(gameBoard)
    for h in range(len(gameBoard)):
        for w in range(width):
            if (gameBoard[w][h] == value):

                #check horizontal
                count = 1
                for i in range(w+1, width):
                    if (gameBoard[i][h] != value):
                        break
                    count += 1
                    
                if (count == connect):
                    return True
                    
                #check vertical
                count = 1
                for j in range(h+1, height):
                    if (gameBoard[w][j] != value):
                        break
                    count += 1

                if (count == connect):
                    return True
                    
                #check diagonal left
                count = 1
                i = w-1
                for i in range(h+1, height):
                    if (i<0):
                        break
                    if (gameBoard[i][j] != value):
                        break

                    count += 1
                    i -= 1

                if (count == connect):
                    return True
                    
                #check diagonal right
                count = 1
                i = w+1
                for j in range(h+1, height):
                    if (i >= width):
                        break
                    if (gameBoard[i][j] != value):
                        break
                    
                    count += 1
                    i += 1

                if (count == connect):
                    return True
                    
                    
    return False

    
def isBoardFull(gameBoard):
    width = len(gameBoard)
    height = len(gameBoard[0])
    
    for w in range(width):
        for h in range(height):
            if (gameBoard[h][w] == '.'):
                return False
                
    return True
    
    
    
parser = argparse.ArgumentParser(description='Play a game of Connect 4 (or more)')

parser.add_argument('-w', '--width', default=7, type=int, help='an integer that sets the width of the board', metavar='int')
parser.add_argument('-he', '--height', default=7, type=int, help='an integer that sets the height of the board', metavar='int')
parser.add_argument('-c', '--connect', default=4, type=int, help='an integer that sets the number of spaces needed to win', metavar='int')
parser.add_argument('-s', '--square', default=0, type=int, help='an integer that sets the width and height of a square board (overrides other parameters)', metavar='int')
parser.add_argument('-l', '--load', default="", type=str, help='a filename with a save game object to be loaded', metavar='filename')

args = parser.parse_args()
#args. height, width, connect, square, load

width = args.width
height = args.height
connect = args.connect
square = args.square
filename = args.load

userWon = False
computerWon = False

sampleData = {'width': 1, 'height': 2, 'connect': 3}
pickle.dump(sampleData, open('sampleData', 'wb'))

#if command line parameter is supplied for load, load a game
if (filename != ''):
    width = 0
    height = 0
    connect = 0
    square = 0
    
    pklFile = open(filename, 'rb')
    pklData = pickle.load(pklFile)
    width = pklData['width']
    height = pklData['height']
    connect = pklData['connect']
    #TODO load the gameboard
    
    pklFile.close()

#load standard game if no command line load parameter    
else:
    if (square != 0):
        width = square
        height = square
        
    if (connect > width and connect > height):
        clearScreen()
        print("A " + str(connect) + "-piece long string will not fit on a " + str(width) + " by " + str(height) + " size board. Nobody can win!\n\n\n")
        sys.exit()
        
    #set the gameboard
    gameBoard = [[EMPTYVAL for x in range(width)] for y in range(height)]
    
userInput = 'x'

#Game Loop
while userInput != 'n':

    clearScreen()

    if (userWon or computerWon):
        resetGameBoard(gameBoard)
        userWon = False
        computerWon = False
        
    printGameBoard(gameBoard)
    
    userInput = input('\n\nEnter column number where you\'d like to drop your piece\n(Enter \'q\' to quit)\n')
    
    print('len(gameBoard) = ' + str(len(gameBoard)))
    print('len(gameBoard[0]) = ' + str(len(gameBoard[0])))
    print('len(gameBoard[0][0])' + str(len(gameBoard[0][0])))
    validateUserInput(gameBoard, userInput)
    
    if (userInput == 'q'):
        sys.exit()
        
    if (userInput == 's'):
        gameData = {'width': width, 'height': height, 'connect': connect, 'gameBoard': gameBoard}
        pickle.dump(gameData, open('gameData', 'wb'))
        userInput = input('\n\nYour game has been saved in the file gameData\n\nType \'c\' to continue...')
        continue

    userMove(userInput, gameBoard)
    
    computerWon = checkWin(gameBoard, connect, COMPVAL)
    userWon = checkWin(gameBoard, connect, PLAYERVAL)
    
    if userWon:
        clearScreen()
        printGameBoard(gameBoard)
        print('\n\n  You win!');
        userInput = input('\n\nWould you like to play again? (y or n)')

    if computerWon:
        clearScreen()
        printGameBoard(gameBoard)
        print('\n\n  You lose...')
        userInput = input('\n\nWould you like to play again? (y or n)')
        
    if isBoardFull(gameBoard):
        clearScreen()
        printGameBoard(gameBoard)
        print('\n\n  Tie game!')
        userInput = input('\n\nWould you like to play again? (y or n)')
    