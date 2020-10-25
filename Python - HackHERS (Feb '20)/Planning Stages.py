# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:00:22 2020

@author: joshc

Sudoku Refresh for 2020

Planning Stage Document

Currently Have:
    Fully functioning Sudoku game with:
        iPython console functionality
        Replay function
        Undo function
        Board Difficulty Selection and limited variety of choices
        
New Features to create:
    Grabbing boards from internet source to not have to manually create
    GUI ->
        Use the mouse to play on a popup window, to free from need to keep Spyder open
    AutoSolver ->
        Use the guessing/backtracking method from 211 Homework first
        Try and figure out another way to do it without the random guess

Updates to existing code:
    Remake the majority of the functions so they are smaller, more singleminded
    Code functions shouldn't do multiple tasks
        This doesn't mean they cannot return multiple things, but every function should do a single concept
    Work through existing algorithms to improve bigO runtime for functions
        History recorder is currently n^3?
        Use improvements from Java 2018 update to bring it down to constant
    Improve documentation of code and functions, so that there is no ambiguity
    
Plan of Action for HackHERS 2020:
    1) Figure out webscraping for board acquisition
        1a) identify how to show board is easy/medium/hard
        1b) rewrite board function from original game to be clearer
    2) GUI Output instead of printBoard function
        2a) Identify library/useful functions for graphical window outputs
        2b) Determine simplicity of adding a pencil mark layer to keep track of possible values
            2bi) Implement pencilmark tracking into board storage to facilitate future guessing programs
    3) Remake codebase with simpler functions/bigO optimization
        3a) Undo Function -> bring from n^3 -> constant time using Java update
        3b) WHat changes need to be made to deal with addiiton of GUI elements
        3c) DOCUMENT YOUR FUNCTIONS USING DOCSTRINGS
    4) Add in the GuessSolver from CS211 Project
        4a) Using basic translation, make sure function doesn't overcome recursive limits
            4ai) 
        4b) Can we use this to find a way to let the program produce a viable
            guess given the current state of the board?

"""


