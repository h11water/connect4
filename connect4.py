from matplotlib import pyplot as plt
from stack import stack #import class stack
import numpy as np
import random

def startgame():
    '''start the game'''
    board = createboard()                #ask board size
    opponentiscomputer = chooseplayer()  #play against computer or player?
    winningposition = playing(board, opponentiscomputer)   #play the game
    highlightwin(winningposition,board)
    return

def chooseplayer():
    '''p vs p OR ai vs p'''
    print("player vs player (P)")
    print("OR player vs computer (C)")
    opponent = (input(":")).upper()
    while(opponent != str and opponent != "C" and opponent != "P"):
        print(opponent != str, opponent != "C" , opponent != "P")
        opponent = input("must be p or c").upper()

    if opponent == "C":
        return True
    else:
        return False
    return False

def createboard():
    '''create an array of stack'''
    maxcolumns = 40
    maxrows = 30

    #input board size
    columns = int(input("number of columns. must be between 7 and 40: "))

    while(type(int(columns)) != int or 7 > columns > maxcolumns):
        columns = int(input("number of columns. must be between 7 and 40: "))

    rows = int(input("number of rows. must be between 6 and 30: "))
    while(type(int(rows)) != int or 6 > rows > maxrows):
         columns = int(input("number of rows. must be between 6 and 30:  "))



    listofstacks = []
    for i in range(columns):#create list of stacks
        listofstacks.append(createstack(rows).returnstack())
    board = (listofstacks)#create array of stacks

    return board

def createstack(rows):
    '''create a stack'''
    s = stack(rows)
    return s

def playing(board, opponentiscomputer):
    '''playing the game'''
    currentplayer = "P1" #player1 starts
    winner = "nobody"
    won = False

    while((boardfull(board) == False)):
        won,winner, winningposition = windetected(board)
        if won:
            break
        haveturn(board, currentplayer)
        currentplayer = nextplayer(currentplayer, opponentiscomputer,board)

    if won == True:
        print(winner, "won")
        return winningposition
    else:
        print("nobody won")
        return False
    return

def windetected(board):
    '''check horizontal, verticals and diagonals for win'''
    #check for connected in vertical, horizontal and diagonal

    won = False
    #check verticals
    won, winner, winningposition = checkvertical(board)

    #check horizontals
    if won != True: #if havent won yet
        won, winner,winningposition = checkhorizontal(board)

    #check diagonals
    if won != True:#if havent won yet
        won, winner, winningposition = createnewboardandcheckdiagonal(board)
    if won == True:
        return True, winner, winningposition
    else:
        return False, winner, winningposition

    return False

def checkvertical(board):
    '''check each column for 4 connected'''
    runlength = 1
    winner = "nobody" #by default nobody wins
    winningposition = ["none"]

    for j in range(len(board)):
        column = board[j].returnlist()
        previousmarker = column[0]

        for i in range(1,len(column)-1):
            if previousmarker == column[i] and previousmarker != "0": #only check the columns that have markers
                runlength += 1
                if runlength == 4:
                    winningposition = ["vertical",j ,i ]
                    print("vertically won")
                    return True, previousmarker, winningposition
            else:
                previousmarker = column[i]
                runlength = 1 #reset the amount of contiguous markers

    return False, winner, winningposition

def checkhorizontal(board):
    '''check each row for 4 connected'''
    runlength = 0
    column, row = 0, 0
    winningposition = ["none"]

    previousmarker = board[column].returnlist()[row]
    for row in range(len(board[0].returnlist())): #length of rows
        for column in range(len(board)):
            if previousmarker == board[column].returnlist()[row] and previousmarker != "0":
                runlength += 1
                if runlength >= 4:
                    print("horizontally won")
                    winningposition = ["horizontal", column, row]
                    return True, previousmarker, winningposition #previousmarker is winner
            else:
                previousmarker = board[column].returnlist()[row]
                runlength = 1

    return False, "nobody", winningposition

    #check first item in first row
    #store item if its a marker
    #compare previous with next
    #runlength +1 if same
    #else reset marker and go to first step

    return False, "nobody"

def createextendedmatrix(board):
    '''create matrix of same row size but column size of (old column + 2*row size)
    and place the board in the middle of new matrix '''

    oldcolumnlength = len(board[0].returnlist())
    oldrowlength = len(board)

    newrowsize = oldrowlength + 2 * oldcolumnlength

    boardinlistoflistform = []

    for column in range(oldrowlength):
        boardinlistoflistform.append(board[column].returnlist()) #create the board in list of list form

    columnofstrings = ["null" for x in range(oldcolumnlength)]

    listoflist = []
    for column in range(newrowsize):
        listoflist.append(columnofstrings)
    extendedmatrix = np.array(listoflist)

    extendedmatrix[oldcolumnlength:oldcolumnlength+oldrowlength] = boardinlistoflistform #place the old matrix at the centre


    return extendedmatrix


def createnewboardandcheckdiagonal(board): #check multiple diagonals

    '''create an longer version of the board and place the old board at the middle of the board
    '''
    extendedmatrix = createextendedmatrix(board)
    won, winner, winningposition = checkdiagonaltotheright(extendedmatrix)
    if won == False: #check diagonal in reverse direction
        won, winner, winningposition = checkdiagnoaltotheleft(extendedmatrix)
    #check the diagonals starting from 0,0 of new board to oldboard row + column
    #do this again but reverse direction


    return won, winner, winningposition

def checkdiagonaltotheright(extendedmatrix): #check 1 diagonal
    '''checkdiagonals starting from down left to top right'''

    winningposition = ["none"]

    previousmarker = extendedmatrix[0][0] #marker at left most end
    rowcolumn = len(extendedmatrix)-len(extendedmatrix[0])-1 #row and collumn have same index
    runlength = 1


    for shift in range(rowcolumn): #shift the diagonal by this much
        for i in range(0,len(extendedmatrix[0])):

            if previousmarker == extendedmatrix[i+shift][i] and previousmarker != "null" and previousmarker != "0":
                runlength += 1
                print("diagonally + 1", previousmarker, runlength)

            else:            #not matching
                previousmarker = extendedmatrix[i+shift][i]
                runlength = 1 #reset counter


            if runlength >= 4:
                print("won diagonally to the right")
                winner = previousmarker
                winningposition = ["torightdiagonal", i, shift-len(extendedmatrix[0])]
                return True, winner, winningposition
    return False, "nobody", winningposition


def checkdiagnoaltotheleft(extendedmatrix):
    '''checkdiagonals starting from down right to top left'''

    winningposition = ["none"]
    matrixheight = len(extendedmatrix[0])-1
    matrixlength = len(extendedmatrix) - 1
    previousmarker = extendedmatrix[matrixlength][0] #marker at right most end

    runlength = 1
    column = matrixlength-matrixheight-1 #-matrixheight because it is not necessary to check the 5leftmost columns

    for shift in range(matrixheight):
        column = matrixlength-matrixheight-1 #reset column
        for row in range(0, matrixheight):

            if previousmarker == extendedmatrix[column-shift][row] and previousmarker != "a" and previousmarker != "null" and previousmarker != "0":

                runlength += 1
                print("diagonally + 1", previousmarker, runlength)

            else:            #not matching
                previousmarker = extendedmatrix[column-shift][row]
                runlength = 1 #reset counter
            column -= 1
            if runlength >= 4:
                print("won diagonally to the left")
                winner = previousmarker
                winningposition = ["toleftdiagonal", column-shift, row]
                return True, winner, winningposition

    return False, "nobody", winningposition

def boardfull(board):
    '''returns if board is full'''
    for column in range(len(board)):
        if board[column].isfull() == False:
            return False
    return True #board is full

def haveturn(board, currentplayer):
    '''let the current player have turn'''
    plotboard(board)
    placemarker(board, currentplayer)

    return

def placemarker(board, currentplayer):
    '''place marker in requested column'''
    column = int(input("which column to place: "))
    while(column < 0 or column > len(board) or board[column].isfull() == True):
        print("that column either does not exist or is full")
        column = input("which column to place: ")

    board[column].push(currentplayer)
    return

def nextplayer(currentplayer, opponentiscomputer, board):
    '''go tho the next player'''
    if (opponentiscomputer == True):
        comphaveturn(board)
        return "P1"

    if (currentplayer == "P1"):
        return("P2")
    else:
        return("P1")

def comphaveturn(board):
    '''computer places in random column'''
    column = random.randint(0,len(board)-1)
    board[column].push("C")
    return


def plotboard(board):
    #create a list of column indexi for each player
    #create a list of row indexi for each player
    P1columns = []
    P2columns = []
    PCcolumns = []

    P1rows = []
    P2rows = []
    PCrows = []
    #search through board
    #if player marker detected, add the index to the appropiate list
    for column in range(len(board)):
        for row in range(len(board[column].returnlist())):
            if board[column].returnlist()[row] == "P1":
                P1columns.append(column)
                P1rows.append(row)
            elif board[column].returnlist()[row] == "P2":
                P2columns.append(column)
                P2rows.append(row)
            elif board[column].returnlist()[row] == "C":
                PCcolumns.append(column)
                PCrows.append(row)

    plt.figure(facecolor= "royalblue")
    plt.xlabel("columns", color = "white")

    column = len(board)
    size = 144 - column*2.3762

    plt.scatter(P1columns, P1rows, s = size, color="red", marker="o")
    plt.scatter(P2columns, P2rows, s = size, color="gold", marker="o")
    plt.scatter(PCcolumns, PCrows, s = size, color="gold", marker="o")

    plt.ylim(-1, len(board[0].returnlist()))
    plt.xlim(-1, len(board))
    plt.show()


    return

def highlightwin(winningposition, board):
    '''highlight win position'''
    x = []
    y= []

    plt.figure(facecolor= "royalblue")
    plt.xlabel("columns", color = "white")

    if winningposition[0] == "vertical":
        for i in range(winningposition[2], winningposition[2]-4, -1):
            x.append(i)
            y.append(winningposition[1])

    elif winningposition[0] == "horizontal":
        for i in range(winningposition[1], winningposition[1]-4, -1):
            print(winningposition[1], winningposition[2], i, i-1)
            x.append(winningposition[2])
            y.append(i)

    elif winningposition[0] == "torightdiagonal":
        j = 0
        for i in range(winningposition[1], winningposition[1]-4, -1):
            x.append(i)
            y.append(winningposition[1]-j)
            j += 1

    elif winningposition[0] == "toleftdiagonal":

        for i in range(winningposition[1]-2, winningposition[1]-2 - 4, -1):
            x.append(i)
        for j in range(winningposition[2] -4, winningposition[2], 1):
            y.append(j)

    elif winningposition[0] == "none":
        return

    column = len(board)
    size = 144 - column*2.3752
    plt.scatter(y, x, s = size, color="deepskyblue", marker="o")

    plt.ylim(-1, len(board[0].returnlist()))
    plt.xlim(-1, len(board))
    plt.show()
    return

startgame()
