# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 13:54:57 2018

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

#Print out current state of board
def boardPrint(current,num,count=0,columnHold=0,columnCount=0,
               rowOut='',rowShow=1,numbers=[]):
    if num == 2:
        dashCount=19
    if num == 3:
        dashCount=37
        
#    Create Column Number String for Header
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

#Choose which box you're in based on Row/Column info    
def boxChoose(row,column,num):
    rowChunk=((row-1)//num)+1
    columnChunk=((column-1)//num)+1
    boxNumber=num*rowChunk+columnChunk-num
    return boxNumber    

#Define row/column/box values for unique checks    
def currentState(current):
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
            
    #   Auto sorts values for win check at end of game
        boardDictSort={}
        for key in boardDict:
            boardDictSort[key]=sorted(boardDict[key])    
    return boardDictSort


StartBoard=[[0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8]]

num = int(len(StartBoard)**0.5)
boardPrint(StartBoard,num)
board=currentState(StartBoard)
pprint.pprint(board)

print('\n\n')

StartBoard=[[0,1,2,3],
            [4,5,6,7],
            [8,7,6,5],
            [4,3,2,1]]

num = int(len(StartBoard)**0.5)
boardPrint(StartBoard,num)
board=currentState(StartBoard)
pprint.pprint(board)