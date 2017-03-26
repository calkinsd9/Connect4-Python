#!/usr/bin/env python

import argparse
import pickle
import os
import sys
from random import randint

#len(gameBoard) == height
#len(gameBoard[0] == width)
#gameBoard[YVAL][XVAL]

EMPTYVAL = '.'
PLAYERVAL = 'x'
COMPVAL = 'o'
inGameCommands = ['s', 'l', 'q']


def clearScreen():
    #clear screen code taken from  http://stackoverflow.com/questions/2084508/clear-terminal-in-python
    #os.system('cls' if os.name == 'nt' else 'clear')
    return
    
def paddingString(padding):
    string = ''
    for i in range(padding):
        string += ' '
    return string

def printGameBoard(gameBoard):
    width = len(gameBoard[0])
    height = len(gameBoard)
    padding = 38 - width
    boardString = paddingString(padding)
    
    print('\n\n')
    print('  _|_|_|                                                      _|      _|  _|')
    print('_|          _|_|    _|_|_|    _|_|_|      _|_|      _|_|_|  _|_|_|_|  _|  _|')
    print('_|        _|    _|  _|    _|  _|    _|  _|_|_|_|  _|          _|      _|_|_|_|')
    print('_|        _|    _|  _|    _|  _|    _|  _|        _|          _|          _|  ')
    print('_|_|_|_|    _|_|    _|    _|  _|    _|    _|_|_|    _|_|_|    _|          _|\n\n')
    
    #column numbers on top
    for i in range(width):
        if (i < 10):
            boardString += ' ' + str(i+1)
        else:
            boardString += str(i+1)
    boardString += '\n' + paddingString(padding) + '|'
    
    #game board
    count = 0
    for row in gameBoard:
        for value in row:
            boardString += value + '|'
            count += 1
            if count == len(gameBoard[0]):
                boardString += '\n' + paddingString(padding) + '|'
                count =0
    boardString = boardString[:-1]
    
    #column numbers on bottom
    for i in range(width):
        if (i < 10):
            boardString += ' ' + str(i+1)
        else:
            boardString += str(i+1)

    print(boardString)

def resetGameBoard(gameBoard):
    rowIndex = 0
    for row in gameBoard:
        gameBoard[rowIndex] = list(map(lambda x: EMPTYVAL, row))
        rowIndex += 1    
    
def isValidMove(gameBoard, userInput):
    iUserInput = int(userInput, 10) - 1
    if (iUserInput >= 0 and iUserInput < len(gameBoard[0])):
        if (gameBoard[0][iUserInput] == EMPTYVAL):
            #debug
            print('Value for valid move is' + str(gameBoard[0][iUserInput]))
            return True
    #debug
    print('Column is full')
    return False
    
def userMove(userInput, gameBoard):
    iUserInput = int(userInput) - 1
    height = len(gameBoard)
    
    for h in range(height):
        if (gameBoard[h][iUserInput] != EMPTYVAL):
            h -= 1
            break
    
    gameBoard[h][iUserInput] = PLAYERVAL
    
def computerCanWinAt(gameBoard, connect):
    width = len(gameBoard[0])
    height = len(gameBoard)
    
    for h in range(height):
        for w in range(width):
            if (gameBoard[h][w] != PLAYERVAL):

                # check the next [connect] spaces. stop if you hit the end of the board or a playervalue
                # count the number of spaces taken
                # if the compvals == connect -1, then check that the space underneath the empty space is the bottom or taken
                # if it is, return the position
                
                #check horizontal
                taken = 1 if gameBoard[h][w] == COMPVAL else 0
                spaces = 1
                for i in range(w+1, width):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (gameBoard[h][i] == PLAYERVAL):
                        break
                    if (gameBoard[h][i] == COMPVAL):
                        taken += 1
                    
                if (taken == connect-1):
                    for i in range(w+1, width):
                        if gameBoard[h][i] == EMPTYVAL:
                            break
                    if (h == height - 1) or ((h+1)<height and (gameBoard[h+1][i] != EMPTYVAL)):
                        return i
                    
                #check vertical
                taken = 1 if gameBoard[h][w] == COMPVAL else 0
                spaces = 1
                for j in range(h+1, height):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (gameBoard[j][w] == PLAYERVAL):
                        break
                    if (gameBoard[j][w] == COMPVAL):
                        taken += 1

                if (taken == connect-1):
                    for j in range(h+1, height):
                        if gameBoard[j][w] == EMPTYVAL:
                            break
                    if (h == height - 1) or ((j+1<height) and gameBoard[j+1][w] != EMPTYVAL):
                        return w
                    
                #check diagonal left
                taken = 1 if gameBoard[h][w] == COMPVAL else 0
                spaces = 1
                i = w-1
                for j in range(h+1, height):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (i<0):
                        break
                    if (gameBoard[j][i] == PLAYERVAL):
                        break
                    if (gameBoard[j][i] == COMPVAL):
                        taken += 1
                    i -= 1

                if (taken == connect-1):
                    i = w-1
                    for j in range(h+1, height):
                        if (gameBoard[j][i] == EMPTYVAL):
                            break
                        i -= 1
                    if (j == height - 1) or ((j+1<height) and gameBoard[j+1][i] != EMPTYVAL):
                        return i

                    
                #check diagonal right
                taken = 1 if gameBoard[h][w] == COMPVAL else 0
                spaces = 1
                i = w+1
                for j in range(h+1, height):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (i >= width):
                        break
                    if (gameBoard[j][i] == PLAYERVAL):
                        break
                    if (gameBoard[j][i] == COMPVAL):
                        taken += 1
                    i += 1

                if (taken == connect-1):
                    i = w+1
                    for j in range(h+1, height):
                        if (gameBoard[j][i] == EMPTYVAL):
                            break
                        i -= 1
                    if (j == height - 1) or ((j+1<height) and gameBoard[j+1][i] != EMPTYVAL):
                        return i
                    
                    
    return -1
    
def userCanWinAt(gameBoard, connect):
    width = len(gameBoard[0])
    height = len(gameBoard)
    
    for h in range(height):
        for w in range(width):
            #debug
            print('usercanwin iteration ' + str(h) + str(w) + 'VAL: ' +str(gameBoard[h][w]))
            if (gameBoard[h][w] != COMPVAL):

                # check the next [connect] spaces. stop if you hit the end of the board or a playervalue
                # count the number of spaces taken
                # if the compvals == connect -1, then check that the space underneath the empty space is the bottom or taken
                # if it is, return the position
                
                #check horizontal
                #debug
                print('checking horizontal')
                taken = 1 if gameBoard[h][w] == PLAYERVAL else 0
                spaces = 1
                for i in range(w+1, width):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (gameBoard[h][i] == COMPVAL):
                        break
                    if (gameBoard[h][i] == PLAYERVAL):
                        taken += 1
                    
                if (taken == connect-1):
                    #debug
                    print('win detected')
                    for i in range(w, width):
                        if gameBoard[h][i] == EMPTYVAL:
                            break
                    if (h == height - 1) or ((h+1)<height and (gameBoard[h+1][i] != EMPTYVAL)):
                        #debug
                        print('at gameBoard' + str(h) + str(i))
                        return i
                    
                #check vertical
                #debug
                print('checking vertical')
                taken = 1 if gameBoard[h][w] == PLAYERVAL else 0
                spaces = 1
                for j in range(h+1, height):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (gameBoard[j][w] == COMPVAL):
                        break
                    if (gameBoard[j][w] == PLAYERVAL):
                        taken += 1

                if (taken == connect-1):
                    #debug
                    print('win detected')
                    for j in range(h, height):
                        #debug
                        print('jw ' + str(j) +str(w) + ' = ' + str(gameBoard[j][w]))
                        if gameBoard[j][w] == EMPTYVAL:
                            #debug
                            print('empty val at' + str(j) + str(w))
                            break
                    if (j == height - 1) or ((j+1<height) and gameBoard[j+1][w] != EMPTYVAL):
                        #debug
                        print('at gameBoard' + str(j) + str(w))
                        return w
                    
                #check diagonal left
                #debug
                print('checking diagonal left')
                taken = 1 if gameBoard[h][w] == PLAYERVAL else 0
                spaces = 1
                i = w-1
                for j in range(h+1, height):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (i<0):
                        break
                    if (gameBoard[j][i] == COMPVAL):
                        break
                    if (gameBoard[j][i] == PLAYERVAL):
                        taken += 1
                    i -= 1

                if (taken == connect-1):
                    #debug
                    print('win detected')
                    i = w-1
                    for j in range(h, height):
                        #debug
                        print('ji ' + str(j) +str(i) + ' = ' + str(gameBoard[j][i]))
                        if (gameBoard[j][i] == EMPTYVAL):
                            #debug
                            print('empty val at' + str(j) + str(i))
                            break
                        i -= 1
                    if (j == height - 1) or ((j+1<height) and gameBoard[j+1][i] != EMPTYVAL):
                        #debug
                        print('at gameBoard' + str(j) + str(i))
                        return i

                    
                #check diagonal right
                #debug
                print('checking diagonal right')
                taken = 1 if gameBoard[h][w] == PLAYERVAL else 0
                spaces = 1
                i = w+1
                for j in range(h+1, height):
                    spaces += 1
                    if spaces > connect:
                        break
                    if (i >= width):
                        break
                    if (gameBoard[j][i] == COMPVAL):
                        break
                    if (gameBoard[j][i] == PLAYERVAL):
                        taken += 1
                    i += 1

                if (taken == connect-1):
                    #debug
                    print('win detected')
                    i = w+1
                    for j in range(h, height):
                        #debug
                        print('ji ' + str(j) +str(i) + ' = ' + str(gameBoard[j][i]))
                        if (gameBoard[j][i] == EMPTYVAL):
                            #debug
                            print('empty val at' + str(j) + str(i))
                            break
                        i -= 1
                    if (j == height - 1) or ((j+1<height) and gameBoard[j+1][i] != EMPTYVAL):
                        #debug
                        print('at gameBoard' + str(j) + str(i))
                        return i
                    
                    
    return -1

    
def computerMove(gameBoard, connect):
    height = len(gameBoard)
    width = len(gameBoard[0])
    
    #AI logic:
    # 1) If I am about to win, move to win
    # 2) If the user needs one move to win, stop her from winning.
    # 3) If neither of the above conditions are met, then
    # 4) If the middle center space on the bottom row isn't taken yet, take it. If it is taken
    # 5) Move randomly

    # 1) Move to win
    #   a) For each space
    #   b) if that space is blank or mine
    #   c) do a win check in all directions but allowing for blank tiles
    #   d) for each successful win check scenario:
    #   e) check if the space below the win space is the bottom of the board or not empty
    #   f) if the space below is filled or the bottom, take the win
    
    compMove = computerCanWinAt(gameBoard, connect)
    #debug
    print('compMove after computerCanWinAt is ' + str(compMove))
    
    if compMove == -1:
        compMove = userCanWinAt(gameBoard, connect)
        
    #debug
    print('compMove after userCanWinAt is ' + str(compMove))    

    if compMove == -1:
        middleOfBoard = (width-1) // 2
        #debug
        print('middleOfBoard is ' + str(middleOfBoard))
        print('gameBoard[' + str(height-1) + '][' + str(middleOfBoard) + '] is ' + str(gameBoard[height-1][middleOfBoard]))
        if (gameBoard[height-1][middleOfBoard] == EMPTYVAL):
            compMove = middleOfBoard
            
    #debug
    print('compMove after middleOfBoard is ' + str(compMove))
    
    if compMove == -1:
        compMove = randint(1,width)
        while not isValidMove(gameBoard, str(compMove)):
            compMove = randint(1,width)
        compMove -= 1
        
        #debug
        print('random compMove is ' + str(compMove))
    
    for h in range(height):
        if (gameBoard[h][compMove] != EMPTYVAL):
            h -= 1
            break
            
    gameBoard[h][compMove] = COMPVAL
    
    
def checkWin(gameBoard, connect, value):
    width = len(gameBoard[0])
    height = len(gameBoard)
    for h in range(height):
        for w in range(width):
            if (gameBoard[h][w] == value):

                #check horizontal
                count = 1
                for i in range(w+1, width):
                    if (gameBoard[h][i] != value):
                        break
                    count += 1
                    
                if (count == connect):
                    #debug
                    print('Win by horizontal')
                    return True
                    
                #check vertical
                count = 1
                for j in range(h+1, height):
                    if (gameBoard[j][w] != value):
                        break
                    count += 1

                if (count == connect):
                    #debug
                    print('Win by vertical')
                    return True
                    
                #check diagonal left
                count = 1
                i = w-1
                for j in range(h+1, height):
                    if (i<0):
                        break
                    if (gameBoard[j][i] != value):
                        break

                    count += 1
                    i -= 1

                if (count == connect):
                    #debug
                    print('Win by diagonal left')
                    return True
                    
                #check diagonal right
                count = 1
                i = w+1
                for j in range(h+1, height):
                    if (i >= width):
                        break
                    if (gameBoard[j][i] != value):
                        break
                    
                    count += 1
                    i += 1

                if (count == connect):
                    #debug
                    print('Win by diagonal right')
                    return True
                    
                    
    return False

    
def isBoardFull(gameBoard):
    width = len(gameBoard)
    height = len(gameBoard[0])
    
    for w in range(width):
        for h in range(height):
            if (gameBoard[h][w] == EMPTYVAL):
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
    gameBoard = pklData['gameBoard']
    
    pklFile.close()

#load standard game if no command line load parameter    
else:
    if (square != 0):
        width = square
        height = square
        
    if (connect > width and connect > height):
        clearScreen()
        print('\n\n\nA ' + str(connect) + '-piece long string will not fit on a ' + str(width) + ' by ' + str(height) + ' size board. Nobody can win!\n\n\n')
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
    
    userInput = input('\n\nEnter column number where you\'d like to drop your piece\n  (Enter \'q\' to quit, \'s\' to save, or \'l\' to load)\n')
    
    invalidInput = True
    
    #while loop ensures valid user input 
    while invalidInput:
        inputIsCommand = userInput in inGameCommands
        
        inputIsInt = True
        try:
            int(userInput, 10)
        except ValueError:
            inputIsInt = False
                            
        if inputIsInt:
            #debug
            print('inputIsInt')
            invalidInput = not isValidMove(gameBoard, userInput)
        else:
            invalidInput = not inputIsCommand

        if invalidInput:
            userInput = input('Input invalid or column is full. Please make another selection.\n\n')
    
    if (userInput == 'q'):
        sys.exit()
        
    if (userInput == 's'):
        gameData = {'width': width, 'height': height, 'connect': connect, 'gameBoard': gameBoard}
        pickle.dump(gameData, open('gameData', 'wb'))
        userInput = input('\n\nYour game has been saved in the file gameData\n\nType \'c\' to continue...')
        continue
        
    if (userInput == 'l'):
        width = 0
        height = 0
        connect = 0
        square = 0
        userWon = False
        computerWon = False
        
        pklFile = open('gameData', 'rb')
        pklData = pickle.load(pklFile)
        width = pklData['width']
        height = pklData['height']
        connect = pklData['connect']
        gameBoard = pklData['gameBoard']
        
        pklFile.close()
        userInput = input('\n\nYour game has been loaded from the gameData file. Type \'c\' to continue...')
        continue
        
    userMove(userInput, gameBoard)
    
    userWon = checkWin(gameBoard, connect, PLAYERVAL)
    
    if not isBoardFull(gameBoard) and not userWon:
        computerMove(gameBoard, connect)
        computerWon = checkWin(gameBoard, connect, COMPVAL)
        
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
    