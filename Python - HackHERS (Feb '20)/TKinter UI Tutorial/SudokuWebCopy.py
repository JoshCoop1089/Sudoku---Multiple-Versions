# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:22:59 2020

@author: joshc
"""


"""
Code copied from http://newcoder.io/gui/
"""
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT
import argparse

MARGIN = 50
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
BOARDDIFF = ["easy", "medium", "hard", "debug", "error"]

class SudokuError(Exception):
    pass
def parseArguments():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--board", help = "Desired board name", 
                           type = str, choices = BOARDDIFF, required = True)
    args = vars(argParser.parse_args())
    return args['board']
class SudokuBoard(object):
    def __init__(self, boardFile):
        self.board = self.__createBoard(boardFile)
    def __createBoard(self, boardFile):
        """
        Parameters
        ----------
        boardFile : a version of a startBoard gotten via webScrape/looking at 
        previous boards

        Returns
        -------
        An NxN array containing the starting info of the board, and locations 
        of the numbers

        """
        board = []
        #iterate over all lines
        for line in boardFile:
            line = line.strip()
            if len(line)!= 9:
                raise SudokuError ("This line is too short")
            board.append([])
            # Fill in the line with digits
            for char in line:
                if not char.isdigit():
                    raise SudokuError("Invalid Character from source")
                board[-1].append(int(char))
        #Raise Error is line number doesn't match expectation
        if len(board) != 9:
            raise SudokuError("Sudoku board is of incorrect size")
        #return the full board
        return board
class SudokuGame(object):
    def __init__(self, boardFile):
        self.boardFile = boardFile
        self.startPuzzle = SudokuBoard(boardFile).board
    def start(self):
        self.gameOver = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.startPuzzle[i][j])
    def winCondition(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.gameOver = True
        return True
    def __checkBlock(self, block):
        return set(block) == set(range(1,10))
    def __check_row(self, row):
        return self.__checkBlock(self.puzzle[row])
    def __check_column(self, column):
        return self.__checkBlock(
            [self.puzzle[row][column] for row in range(9)])
    def __check_box(self, row, column):
        return self.__checkBlock([ self.puzzle[r, c] 
                                  for r in range(row*3, (row+1)*3)
                                  for c in range(column * 3, (column+1) * 3)])
class SudokuUI(Frame):
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)
        self.row, self.col = -1,-1
        self.__initUI()
    def __initUI(self):
        self.parent.title("Sudoku Game")
        self.pack(fill = BOTH)
        self.canvas = Canvas(self, width = WIDTH, height = HEIGHT)
        self.canvas.pack(fill = BOTH, side = TOP)
        clear_button = Button(self, text = "Reset Board", 
                              command = self.__clearAnswers)
        clear_button.pack(side = LEFT)
        undoButton = Button(self, text = "Undo Last Move", 
                            command = self.__undoLastMove)
        undoButton.pack(side = LEFT, fill = BOTH)
        self.__drawGrid()
        self.__drawPuzzle()
        self.canvas.bind("<Button-1>", self.__cellClicked)
        self.canvas.bind("<Key>", self.__keyPressed)
    def __drawGrid(self):
        for i in range(10):
            color = "blue" if i%3 == 0 else "gray"
            
            #Creating the vertical lines, using color to distinquish boxes
            x0 = MARGIN + i*SIDE
            y0 = MARGIN
            x1 = MARGIN + i*SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill = color)
            
            #Creating the horizontal lines, using color to distinguish boxes
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill = color)
    def __drawPuzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE/2
                    y = MARGIN + i * SIDE + SIDE/2
                    original = self.game.startPuzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x,y,text = answer, tags = "numbers", fill = color)
    def __clearAnswers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__drawPuzzle()
    def __undoLastMove(self):
        pass
    def __cellClicked(self, event):
        if self.game.gameOver:
            return
        x, y = event.x, event.y
        if(MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()
            
            #Get row/col from x,y coordinates
            row, col = int((y-MARGIN) / SIDE), int((x - MARGIN) / SIDE)
            
            #if cell already selected, deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        self.__drawCursor()
    def __drawCursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline = "red", tags = "cursor")
    def __keyPressed(self, event):
        if self.game.gameOver:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__drawPuzzle()
            self.__drawCursor()
            if self.game.winCondition():
                self.__drawVictory()
    def __drawVictory(self):
        x0=y0 = MARGIN + SIDE*2
        x1=y1 = MARGIN + SIDE*7
        self.canvas.create_oval(
            x0,y0,x1,y1,tags = "victory", fill = "dark orange", outline = "orange")
        x = y = MARGIN + 4 * SIDE + SIDE/2
        self.canvas.create_text(
            x,y,text = "You WIN!", tags = "winner", fill = "white", font = ("Arial", 32))

if __name__ == '__main__':
    board_name = parseArguments()
    with open('%s.sudoku' %board_name, 'r') as boards_file:
        game = SudokuGame(boards_file)
        game.start()
        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" %(WIDTH, HEIGHT + 40))
        root.mainloop()