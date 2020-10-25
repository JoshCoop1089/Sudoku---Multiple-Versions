# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 12:54:57 2018
commit test comment via ATOM text editor
commit test comment via Spyder IDE
@author: joshc

Stage 1 (Base Game)
    -- Complete -- (5/27/18)
    Print Board
    Unique Identifiers
    Undo
    Number Placement
    Occupied Spot
    Win State

Stage 2 (Practice Data Import)
    --Complete-- (6/3/18)
    Import premade boards from multiple files
        (chooseBoardSize function)
    Choice of random board of requested size/difficulty
            (4x4 or 9x9 easy,medium,hard)
        (chooseRandomBoard function)

Stage 3 (Hardcoding is bad mkay)
    --Complete-- (6/3/18)
    Scalability, reformat code to work for board size n^2
        (Include 4x4,9x9 test cases)
    Rework box identification code to create box list on fly
        (currentState function)
    Rework box identification for boardPrint function
        (boardPrint function)
    Rework box identification after row column choice for unique checks
        (boxChoose function)

Stage 3a (Update base game code)
    -- Complete -- (6/7/18)
    Rewrite Stage 1 game with Stage 2/3 additions
    Replay feature with new board import from file

Stage 3b (Optimize base code and clean up writing)
    Switch boardDict function to non quadratic version, attempt to use linear
        version of coding by figuring out a way to replace single values instead
        of recreating full dict every round
    Erase duplicates in error messages
    Change win function to identify lack of seros on board instead of using boardDictSort?
    Go through another round of glassbox error checks to make sure that all paths
        are clean, no new bugs from old copies
    Create board class and rewrite function to use methods instead of overt
        loops on regular objects

Stage 4 (Multiple Language Practice, syntax doesn't change logic flow)
    (ETA July)
    Rewrite in Java
        (Such a small step... ffs)

Stage 5 (Visualization Practice)
    (ETA August)
    Develop GUI for output
    Change visual output to only show current board,  as opposed to
        current IPython print outs where every previous step remains.

Stage 6 (Computer solve and Player Board Creation)
    (ETA September)
    Computer solve puzzle, hardcode tactics for number choice reduction
    Computer suggested hint for next possible move, show as different
        typeface from input or blank digits
    Player creates own board either from direct input or
        random selection of starting numbers:
            Choose board size
            Choose random or manual placement
            Input prompts for numbers due to board size (1-4, or 1-9)
                If choose manual, prompt row,column choice after each input,
                    with unique checks running after every place
                If choose random, player inputs number of numbers
                    (ie one 1, three 2's, one 3, four 4's)
                    Program places all chosen numbers in a list, populates
                        missing slots with zero's, chooses a random number from
                        the list and places it in a random row,
                    unique checks and box/row/column allowed numbers check
                        would be helpful
                    prompt warning that randomly created board might not
                        be solvable

Stage 7 (Machine Learning Step)
    (ETA ????)
    Train network to play by using initial game state and final rules

"""


#Deepcopy of list of lists, allows for changes to not change original list
import copy

#Allows for choice of random board from included selection
import random


##AutoWin Board for final loop checking
#StartBoard=[[1,2,3,4],
#            [4,3,2,1],
#            [2,1,4,3],
#            [3,4,1,0]]


                    #                  #
                    ##Helper Functions##
                    #                  #
#For all functions, current is the current board state,          #
#   boardDict is a dictionary of keys for rows,columns and boxes #
#   number, row, and column come from user input, and            #
#   gameHistory shows all previous game states                   #
#   gameCount is the current iteration of the board              #



#Board Size/Difficulty Selection
def chooseBoardSize(boardChosen=False, boardDiffChosen=False):
    while boardChosen == False:
        try:
            boardType=int(input('Please pick which type of board you want to play.'+
                        '\n Input 4 for a 4x4 game, or 9 for a 9x9 game.'+
                        '\n Input 99 to quit. ===> '))
            if boardType != 4 and boardType != 9 and boardType != 99:
                raise IndexError
            elif boardType == 99:
                break
            num=int(boardType)

        #  4x4 Boards
            if boardType == 4:
                fileName='4x4.txt'

        #  9x9 Boards with difficulty selector
            elif boardType == 9:
                while boardDiffChosen == False:
                    try:
                        boardDiff=str(input('What level difficulty would you like to'+
                                        ' try?\n Input e for easy, m for medium, or'+
                                        ' h for hard.\n Input q to quit. ===> '))
                        if (boardDiff != 'e' and boardDiff != 'm'
                                and boardDiff != 'h' and boardDiff != 'q'):
                            raise IndexError
                        boardDiffChosen=True
                        if boardDiff == 'q':
                            StartBoard=[]
                            break
                        elif boardDiff == 'e':
                            fileName='9x9 Easy.txt'
                        elif boardDiff == 'm':
                            fileName='9x9 Medium.txt'
                        elif boardDiff == 'h':
                            fileName='9x9 Hard.txt'
                    except IndexError:
                        print('Please enter the letter e, m, or h to choose'+
                              ' a difficulty, or q to quit.')
                    except ValueError:
                        print('Please enter the letter e, m, or h to choose'+
                              ' a difficulty, or q to quit.')

        #  Load selected board size/difficulty if one has been chosen
            boardChosen=True
            if (boardDiffChosen == False or
                    (boardDiffChosen == True and boardDiff != 'q')):
                StartBoard=chooseRandomBoard(fileName,num)
                print('\n\nThe board you selected looks like:\n')
                boardPrint(StartBoard,int(len(StartBoard)**0.5))
                startCheck=False
                while startCheck == False:
                    try:
                        check=str(input('Would you like to play on this board?'+
                                ' Input y to start your game, or n to '+
                                'choose another board. ===> '))
                        if check == 'y':
                            startCheck=True
                        elif check == 'n':
                            StartBoard=[]
                            startCheck=True
                            boardChosen=False
                        else:
                            raise IndexError
                    except IndexError:
                        print('Please enter either y or n.')
                    except ValueError:
                        print('Please enter either y or n.')
        except IndexError:
            print('\nPlease enter either 4 or 9 to choose a board size, or 99 to quit.')
        except ValueError:
            print('\nPlease enter either 4 or 9 to choose a board size, or 99 to quit.')

#  Error handling for quitting during selection process
    try:
        if StartBoard != []:
            return StartBoard
    except:
        print('')

#Random selection of board after size/difficulty chosen
def chooseRandomBoard(fileName,num,count=0):
#  Import file and seperate individual board strings
    fh=open(fileName,'r')
    inputs=fh.readlines()
    fh.close()
    splited=inputs[0]
    splited=splited.split(' ')

#  Turn individual board strings into dictionary of board lists
    listDict={}
    for board in splited:
        y=[list(map(int,x)) for x in board]
        z=[]
        for i in y:
            z.extend(i)
        listDict[count]=z
        count+=1
    for i in listDict:
        listDict[i].append(9)


#  Split board lists into rows
    numhold=0
    count=0
    interBoard={}
    for i in range(len(splited)):
        numhold=0
        for j in range(num):
            interBoard[count]=listDict[i][numhold:num+numhold]
            count+=1
            numhold+=num


#  Create dictionary of complete boards from groups of rows
    numhold=0
    count=0
    board={}
    while numhold<len(interBoard):
        for i in range(numhold,num+numhold):
            try:
                board[count].append(interBoard[i])
            except KeyError:
                board[count]=[interBoard[i]]
        count+=1
        numhold+=num

#  Choose random board from complete board dictionary
#    Only 5 boards loaded per type, thus randint(0,4) doesn't need scaling
    a=random.randint(0,4)
    boardc=board[a]
    return boardc


#Print out current state of board
def boardPrint(current,num,count=0,columnHold=0,columnCount=0,
               rowOut='',rowShow=1,numbers=[]):
    dashCount=num*(3*num+3)+1

#  Create Column Number String for Header
    for i in range(1,len(current)+1):
        numbers.append(i)
    columnDict={}
    while columnCount<num:
        columnDict[columnCount]='  '.join(map(str,
                                          numbers[columnHold:num+columnHold]))
        columnHold+=num
        columnCount+=1
    columnList=''
    for key in columnDict:
        columnList+=columnDict[key]+'     '

#  Board Header
    print(' '*int(dashCount/2)+'  Column #')
    print('||Row   '+str(columnList))
    print('\/ # '+'-'*dashCount)

#  Board Internals
    boardChunk={}
    for i in range(len(current)):
        numhold=0
        for j in range(num):
            boardChunk[count]=current[i][numhold:num+numhold]
            count+=1
            numhold+=num
    numhold=0
    while rowShow<=len(current):
        for i in range(numhold,num+numhold):
            rowOut+=' | '+str(boardChunk[i])
        print('   '+str(rowShow)+rowOut+' |')
        numhold+=num
        rowShow+=1
        rowOut=''
        if rowShow%num==1:
            print('     '+'-'*dashCount)

#Choose which box you're in based on Row/Column info
def boxChoose(row,column,num):
    rowChunk=((row-1)//num)+1
    columnChunk=((column-1)//num)+1
    boxNumber=num*(rowChunk-1)+columnChunk
    return boxNumber

#Define row/column/box values for unique checks
def currentState(current,num):
    boardDict={}
    for i in range(len(current)):

    #  Create Row Keys and Values
        boardDict['Row '+str(i+1)]=current[i]

    #  Create Column Keys and Values
        helperColumn=[]
        for j in range(len(current)):
            helperColumn.append(current[j][i])

        #  Create Box Keys and Values
            try:
                boardDict['Box '+str(boxChoose(i+1,j+1,num))].append(current[i][j])
            except KeyError:
                boardDict['Box '+str(boxChoose(i+1,j+1,num))]=[current[i][j]]

        boardDict['Column '+str(i+1)]=helperColumn

    #  Auto sorts values for win check at end of game
        boardDictSort={}
        for key in boardDict:
            boardDictSort[key]=sorted(boardDict[key])
    return boardDictSort

#Unique Number Checks
def rowUnique(number,row,boardDict):
    if number in boardDict['Row '+str(row)]:
        return False
    else:
        return True

def columnUnique(number,column,boardDict):
    if number in boardDict['Column '+str(column)]:
        return False
    else:
        return True

def boxUnique(number,box,boardDict):
    if number in boardDict['Box '+str(box)]:
        return False
    else:
        return True

#Game History Recorder for Undo Function
def gameState(current, gameHistory, gameCount):
    gameCount+=1
    gameHistory[gameCount]=copy.deepcopy(current)
    return gameHistory,gameCount

#Creates a random StartBoard
def boardStart():
    StartBoard=chooseBoardSize()
    try:
        num = int(len(StartBoard)**0.5)
        gameHistory={}
        gameHistory[0]=copy.deepcopy(StartBoard)
        current=copy.deepcopy(StartBoard)
        return StartBoard,num,gameHistory,current
    except:
        print('')


#Main Game Function
def letsPlaySudoku(gameCount=0,holdNum=0,undoCheck=False,
                       gameOver=False,replayCheck=False):

    print("\nWelcome to Josh's Sudoku Game!")
    print("\nThis is the Stage 3a version.")
    print("Any spot with a 0 is an 'empty' spot, "
          +"and can have a number placed in it.")

#  Initialize first board
    try:
        StartBoard,num,gameHistory,current=boardStart()
    except:
        gameOver=True
        print("Guess we're not playing today?")

#  Main Game Loop
    while gameOver == False:
        if gameCount%4 == 0:
            print("\nIf you want to quit, enter 99 for Row, Column or Number.")
            print("If you want to undo previous moves, or choose a new row or "
                  +"\ncolumn, enter 88 for Row, Column or Number.")

    #  Undo Loop
        while undoCheck == True and gameCount>=1:
            try:
                undo=str(input("Would you like to undo a move? Input 'y' "
                      +"to undo or 'n' to go back to number placement. ===> "))
                if undo == 'y':
                    gameCount-=1
                    print('\nThe board now looks like: \n')
                    boardPrint(gameHistory[gameCount],num)
                    current=copy.deepcopy(gameHistory[gameCount])
                    if gameCount == 0:
                        undoCheck=False
                        print("\nLooks like we're back at the start.\
                              \nLet's try this board again shall we?")
                elif undo == 'n':
                    undoCheck=False
                    print('\nOK! Back to the game!')
                else:
                    raise IndexError
            except IndexError:
                print("\nPlease enter the letter 'y' to undo a move, "
                      +"or 'n' to go back to number placement.")
            except ValueError:
                print("\nPlease enter the letter 'y' to undo a move, "
                      +"or 'n' to go back to number placement.")

    #  Current state of game for internal checks
        boardDict=currentState(current,num)

    #  Win Condition
        win=[i+1 for i in range(len(StartBoard))]
        if all(key == win for key in boardDict.values()):
            print('\n\n'+' !! '*13)
            print(" !! Congratulations! You've finished this board! !!")
            print(' !! '*13+'\n')
            boardPrint(current)
            print('\nThanks for playing! More immersive features are\
                  planned in the next stage. Stay tuned!')
            while replayCheck == False:
                try:
                    replay=str(input('Would you like to play a new board? '+
                                 ' Input y to start over, or n to end the program. ===> '))
                    if replay == 'n':
                        replayCheck=True
                    elif replay == 'y':
                        StartBoard,num,gameHistory,current=boardStart()
                        replayCheck=True
                    else:
                        raise IndexError
                except IndexError:
                    print('Input y to play again, or n to end the program.')
                except ValueError:
                    print('Input y to play again, or n to end the program.')
            if replay == 'n':
                break

    #  Print Board
        print('\n\n'+'-   -'*7)
        print('The current state of the board is:\n')
        boardPrint(current,num)

    #  Number Placement Loop
        rowCheck=False
        columnCheck=False
        numberCheck=False
        boxChosen=False

    #  Row Input
        while rowCheck == False:
            try:
                row=int(input('Choose a Row    ===> '))
                if ((row>len(StartBoard) or row<1)
                        and (row!=99) and (row!=88)):
                    raise IndexError
                rowCheck = True
                if row == 88:
                    columnCheck,numberCheck=\
                    True,True
                    undoCheck=True
                elif row == 99:
                    columnCheck,numberCheck=\
                    True,True
                    gameOver=True
            except IndexError:
                print('Please input a row number between 1 and 4, '
                      +'99 to quit, or 88 to undo a move.')
            except ValueError:
                print('Please input a row number between 1 and 4, '
                      +'99 to quit, or 88 to undo a move.')

    #  Column Input
        while columnCheck == False:
            try:
                column=int(input('Choose a Column ===> '))
                if ((column>len(StartBoard) or column<1)
                        and (column!=88) and (column!=99)):
                    raise IndexError
                columnCheck=True
                if column == 88:
                    numberCheck=True
                    undoCheck=True
                elif column == 99:
                    numberCheck=True
                    gameOver=True
            except IndexError:
                print('Please input a column number between 1 and 4, '
                      +'99 to quit, or 88 to undo a move.')
            except ValueError:
                print('Please input a column number between 1 and 4, '
                      +'99 to quit, or 88 to undo a move.')

    #  Number already present at Row/Column Choice
        if (gameOver == False and undoCheck == False and
                current[row-1][column-1]!=0):
            try:
                nonEmpty=str(input("\nThere is already a number in Row "
                    +str(row)+", Column "+str(column)
                    +"\n\nWould you like to replace it, or choose another spot"
                    +" on the board? Please input the letter 'r' to "
                    +"replace the number,or 'c' to choose another spot. ===> "))
                if nonEmpty == 'c':
                #  Required to skip over rest of loop and restart at row choice
                    row=0
                    numberCheck=True
                elif nonEmpty == 'r':
                    holdNum=current[row-1][column-1]
                    current[row-1][column-1]=0
                    boardDict=currentState(current)
                else:
                    raise IndexError
            except IndexError:
                print("Please enter the letter 'c' to choose another spot, "
                      +"or 'r' to replace the number.")
            except ValueError:
                print("Please enter the letter 'c' to choose another spot, "
                      +"or 'r' to replace the number.")

    #  Box Selection
        while undoCheck == False and gameOver == False and boxChosen == False:
            box=boxChoose(row,column,num)
            boxChosen=True


    #  Number Input
        while numberCheck == False:
            try:
                number=int(input('Choose a Number ===> '))
                if ((number>len(StartBoard) or number <1)
                        and (number!=88) and (number!=99)):
                    raise IndexError
                if number == 88:
                #  Required to fix replace/undo bug which messes with history
                    if holdNum!=0:
                        current[row-1][column-1]=holdNum
                        boardDict=currentState(current)
                        gameHistory,gameCount=gameState(current,
                                                        gameHistory, gameCount)
                        holdNum=0
                    numberCheck=True
                    undoCheck=True
                elif number == 99:
                    numberCheck=True
                    gameOver=True

            #  Non Unique Number Choice
                elif not rowUnique(number,row,boardDict):
                    print('This number conflicts with another number in Row '
                          +str(row)+'\nPlease choose a new number to place in '
                          +'Row '+str(row)+', Column '+str(column))
                elif not columnUnique(number,column,boardDict):
                    print('This number conflicts with another number in Column '
                          +str(column)+'\nPlease choose a new number to place in '
                          +'Row '+str(row)+', Column '+str(column))
                elif not boxUnique(number,box,boardDict):
                    print('This number conflicts with another number in Box '
                          +str(box)+'\nPlease choose a new number to place in '
                          +'Row '+str(row)+', Column '+str(column))

            #  Unique Number Choice
                else:
                    numberCheck=True
            except IndexError:
                print('Please input a number between 1 and 4, '
                      +'99 to quit, or 88 to undo a move.')
            except ValueError:
                print('Please input a number between 1 and 4, '
                      +'99 to quit, or 88 to undo a move.')

    #  Early Game Quit and Replay Check
        if gameOver:
            print('Looks like you want to stop playing this board.')
            replayCheck=False

        #  Replay Check
            while replayCheck == False:
                try:
                    replay=str(input('Would you like to play a new board? '+
                                 ' Input y to start over, or n to end the program. ===> '))
                    if replay == 'n':
                        replayCheck=True
                    elif replay == 'y':
                        StartBoard,num,gameHistory,current=boardStart()
                        row=0
                        gameOver=False
                        replayCheck=True
                    else:
                        raise IndexError
                except IndexError:
                    print('Input y to play again, or n to end the program.')
                except ValueError:
                    print('Input y to play again, or n to end the program.')
        #  Game Over
            if replay == 'n':
                break

    #  Undo Check
        if undoCheck and gameCount == 0:
            print("\nYou haven't made a move yet!\nLet's try the board again!")
            undoCheck=False
            row=0
        if undoCheck and gameCount>=1:
            row=0

    #  Unique Number Placement and History Recorder
        if row != 0:
            if (rowUnique(number,row,boardDict)
                    and columnUnique(number,column,boardDict)
                    and boxUnique(number,box,boardDict)
                    and current[row-1][column-1] == 0):

            #  Replace 'Empty' ie 0 with chosen number
                current[row-1][column-1]=number

            #  Store new game board into history dictionary for possible undo
                gameHistory,gameCount=gameState(current, gameHistory, gameCount)
                print('\n\n'+'-   -'*7)


letsPlaySudoku()
