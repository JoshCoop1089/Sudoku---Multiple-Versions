# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 10:41:11 2018

@author: joshc

Stage 1 (Base Game) -- Complete -- (5/27/18)
    Print Board
    Unique Identifiers
    Undo
    Number Placement
    Occupied Spot
    Win State
                
Stage 2 (Practice Data Import)
    (ETA end of May)
    Implement class organizing system for main/subclass operations
    Replay feature with new board import from file
    Create file with premade 2x2 start boards and have a system for
        labeling inside file to turn into a dictionary for random 
        selection in main game

Stage 3 (Hardcoding is bad mkay)
    (ETA middle of June)
    Scalability, reformat code to work for board size n^2
        (Include 4x4,9x9 and 16x16 [hexadecimal] test cases)
        Use parent/sub classes
    Rework box identification code to create box list on fly 
    Rework box identification for printBoard function 
    Rework box identification after row column choice for unique checks
    Choice of easy medium hard boards
    Import premade boards from multiple files, figure out how to condense 
        into one file import

Stage 4 (Multiple Language Practice, syntax doesn't change logic flow)
    (ETA July)
    Rewrite in Java
        (Such a small step... ffs)
    
Stage 5 (Visualization Practice)
    (ETA August)
    Develop GUI for output 
    Change visual output to only show current board,  as opposed to 
        current IPython print outs where every previous step remains.

Stage 6 (Complexity in algorithmic solving increases)
    (ETA September)
    Computer solve puzzle, hardcode tactics for number choice reduction
    Computer suggested hint for next possible move, show as different
        typeface from input or blank digits

Stage 7 (Machine Learning Step)
    (ETA ????)
    Train network to play by using initial game state and final rules

"""

#Deepcopy of list of lists, allows for changes to not change original list
import copy


#Hardcoded Start Board, fix in Stage 2 via file imports
StartBoard=[[1,0,0,0],
            [0,0,2,0],
            [0,0,0,3],
            [0,4,0,0]]

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

#Print Board
    #Hardcoded Box Definitions, fix in Stage 3  
def boardPrint(current):
    print('           Column #')
    print('        1  2     3  4')
    print('     -------------------')
    print('R  1 | '+str(current[0][0:2])+' | '+str(current[0][2:4])+' |')
    print('o  2 | '+str(current[1][0:2])+' | '+str(current[1][2:4])+' |')
    print('w    -------------------')
    print('   3 | '+str(current[2][0:2])+' | '+str(current[2][2:4])+' |')
    print('#  4 | '+str(current[3][0:2])+' | '+str(current[3][2:4])+' |')
    print('     -------------------')
    
#Create Row,Columns,Boxes for digit checks 
    #   Want to try and figure out how to replace a single
    #    part of a value list after every placement, instead of 
    #    recreating the dictionary from scratch every time.
    #    Can probably just make a loop to check for row, column 
    #    and box keys and append it but that seems inefficient
def currentState(current,boardDict={}):
    for i in range(len(StartBoard)):
   
    #  Create Row Keys and Values
        boardDict['Row '+str(i+1)]=current[i]
        
    #  Create Box Keys and Values
        #  Hardcoded Box Definitions, fix in Stage 3  
        helperBox=[]
        if i == 0:
            helperBox.extend(current[0][0:2])
            helperBox.extend(current[1][0:2])
        elif i == 1:
            helperBox.extend(current[0][2:4])
            helperBox.extend(current[1][2:4])
        elif i == 2:
            helperBox.extend(current[2][0:2])
            helperBox.extend(current[3][0:2])
        elif i == 3:
            helperBox.extend(current[2][2:4])
            helperBox.extend(current[3][2:4])
        boardDict['Box '+str(i+1)]=helperBox
        
    #  Create Column Keys and Values
        helperColumn=[]    
        for j in range(len(StartBoard)):
            helperColumn.append(current[j][i])
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

#Main Game Function
def letsPlaySudoku(current=copy.deepcopy(StartBoard),gameHistory={},
                   gameCount=0,holdNum=0,undoCheck=False,gameOver=False):
    
    print("\nWelcome to Josh's Sudoku Game!")
    print("\nThis is the Stage 1 version.")
    print("Any spot with a 0 is an 'empty' spot, "
          +"and can have a number placed in it.")
   
    gameHistory[0]=copy.deepcopy(StartBoard)
    
#  Main Game Loop  
    while gameOver == False:
        if gameCount%4 == 0:
            print("\nIf you want to quit, enter 99 for Row, Column or Number.")
            print("If you want to undo previous moves, or choose a new row or "
                  +"column, enter 88 for Row, Column or Number.")  
            
    #  Undo Loop       
        while undoCheck == True and gameCount>=1:
            try:
                undo=str(input("Would you like to undo a move? Input 'y' "
                      +"to undo or 'n' to go back to number placement. ===> "))
                if undo == 'y':
                    gameCount-=1
                    print('\nThe board now looks like: \n')
                    boardPrint(gameHistory[gameCount])
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
        boardDict=currentState(current)  
        
    #  Win Condition
        win=[i+1 for i in range(len(StartBoard))]
        if all(key == win for key in boardDict.values()):
            print('\n\n'+' !! '*13)
            print(" !! Congratulations! You've finished this board! !!")
            print(' !! '*13+'\n')
            boardPrint(current)
            print('\nThanks for playing! More immersive features are\
                  planned in the next stage. Stay tuned!')
            gameOver=True
            break
        
    #  Print Board funtion hardcoded, fix in Stage 3
        print('\n\n'+'-   -'*7)
        print('The current state of the board is:\n')
        boardPrint(current)
         
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
                
    #   Number already present at Row/Column Choice        
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
            

            
    #  Hardcoded Box Definitions, fix in Stage 3   
        while undoCheck == False and gameOver == False and boxChosen == False:
            if row < 3 and column < 3:
                box=1
            elif row < 3 and column > 2:
                box=2
            elif row > 2 and column < 3:
                box=3
            elif row > 2 and column > 2:
                box=4
            boxChosen=True
            
            
    # Number Input
        while numberCheck == False:
            try:
                number=int(input('Choose a Number ===> '))
                if ((number>len(StartBoard) or number <1) 
                        and (number!=88) and (number!=99)):
                    raise IndexError
                if number == 88:
                #   Required to fix replace/undo bug which messes with history
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
                    
            #   Non Unique Number Choice                    
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
                
    #  Early Game Quit    
        #   Will need to check for player starting new board
        #   or same board again in Stage 2    
        if gameOver:
            print("Goodbye! Come play again!")
            break
        
    #   Undo Check
        if undoCheck and gameCount == 0:
            print("\nYou haven't made a move yet!\nLet's try the board again!")
            undoCheck=False
            row=0
        if undoCheck and gameCount>=1:
            row=0
                    
    #    Unique Number Placement and History Recorder
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