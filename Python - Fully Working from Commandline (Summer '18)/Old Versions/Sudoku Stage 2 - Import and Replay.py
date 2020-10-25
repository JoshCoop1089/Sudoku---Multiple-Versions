# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 19:56:58 2018

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
    --Complete-- (6/3/18)
    Import premade boards from multiple files        
        (chooseBoardSize function)
    Choice of random board of requested size/difficulty
            (4x4 or 9x9 easy,medium,hard)
        (chooseRandomBoard function)
        
    --To Do--    
    Implement class organizing system for main/subclass operations (OOP Practice?)

Stage 3 (Hardcoding is bad mkay)
    (ETA middle of June)
    --Complete-- (6/3/18)
    Scalability, reformat code to work for board size n^2
        (Include 4x4,9x9 test cases)     
    Rework box identification code to create box list on fly
        (currentState function)
    Rework box identification for boardPrint function 
        (boardPrint function)
    Rework box identification after row column choice for unique checks
        (boxChoose function)
    
    --To Do--
    Use parent/sub classes (needed? or just good practice on OOP?)
    
Stage 3a (Update base game code)
    Rewrite Stage 1 game with Stage 2/3 additions
    Replay feature with new board import from file
    
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

import pprint
import random

#Board Size/Difficulty Selection
def chooseBoardSize(boardChosen=False, boardDiffChosen=False):
    while boardChosen == False:
        try:
            boardType=int(input('Please pick which type of board you want to play.'+
                        ' Input 4 for a 4x4 game, or 9 for a 9x9 game.'+
                        ' Input 99 to quit. ===> '))
            if boardType != 4 and boardType != 9 and boardType != 99:
                raise IndexError
            elif boardType == 99:
                break
            num=int(boardType)
            
        #    4x4 Boards
            if boardType == 4:
                fileName='4x4.txt'
                
        #    9x9 Boards with difficulty selector
            elif boardType == 9:
                while boardDiffChosen == False:
                    try:
                        boardDiff=str(input('What level difficulty would you like to'+
                                        ' try? Input e for easy, m for medium, or'+
                                        ' h for hard. Input q to quit. ===> '))
                        if (boardDiff != 'e' and boardDiff != 'm' 
                                and boardDiff != 'h' and boardDiff != 'q'):
                            raise IndexError
                        boardDiffChosen=True
                        if boardDiff == 'q':
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
                        
        #    Load selected board size/difficulty if one has been chosen
            boardChosen=True
            if (boardDiffChosen == False or 
                    (boardDiffChosen == True and boardDiff != 'q')):
                StartBoard=chooseRandomBoard(fileName,num)
        except IndexError:
            print('Please enter either 4 or 9 to choose a board size, or 99 to quit.')
        except ValueError:
            print('Please enter either 4 or 9 to choose a board size, or 99 to quit.')
            
#    Error handling for quitting during selection process
    try:
        return StartBoard
    except:
        print('\nCome back and play again!')
        
#Random selection of board after size/difficulty chosen        
def chooseRandomBoard(fileName,num,count=0):
#   Import file and seperate individual board strings     
    fh=open(fileName,'r')
    inputs=fh.readlines()
    fh.close()
    splited=inputs[0]
    splited=splited.split(' ')
    
#    Turn individual board strings into dictionary of board lists
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
   
    
#    Split board lists into rows
    numhold=0   
    count=0
    interBoard={}
    for i in range(len(splited)):
        numhold=0
        for j in range(num):
            interBoard[count]=listDict[i][numhold:num+numhold]
            count+=1
            numhold+=num

    
#   Create dictionary of complete boards from groups of rows 
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
        
#    Choose random board from complete board dictionary 
#      Only 5 boards loaded per type, thus randint(0,4) doesn't need scaling   
    a=random.randint(0,4)
    boardc=board[a]
    return boardc

#Print out current state of board
def boardPrint(current,num,count=0,columnHold=0,columnCount=0,
               rowOut='',rowShow=1,numbers=[]):
    if num == 2:
        dashCount=19
    if num == 3:
        dashCount=37
        
#    Create Column Number String
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
        
#   Board Header        
    print(' '*int(dashCount/2)+'  Column #')
    print('||Row   '+str(columnList))
    print('\/ # '+'-'*dashCount)
    
#   Board Internals 
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

StartBoard=chooseBoardSize()
try:
    chunk = int(len(StartBoard)**0.5)
    boardPrint(StartBoard,chunk)
except:
    print('Quitter')