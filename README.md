[![Travis CI](https://travis-ci.com/B-T-D/TicTacToe_AI.svg?branch=master)](https://travis-ci.com/github/B-T-D/https://travis-ci.com/github/B-T-D/TicTacToe_AI)
[![Coverage Status](https://coveralls.io/repos/github/B-T-D/TicTacToe_AI/badge.svg?branch=master)](https://coveralls.io/github/B-T-D/TicTacToe_AI?branch=master)

# TicTacToe_Minimax
Plays tic tac toe using a game tree and minimax algorithm to find optimal moves. 

Includes a command line interface that supports human vs. computer, human vs. human, and computer vs. computer games. The AI should play a perfect game every time--always tie or win.

# Background
I wanted to implement a minimax game-tree algorithm all the way through to a useable piece of software. In addition to playing with minimax, I wanted to apply good object-oriented programming practices as best I could, and do it from scratch with minimal external dependency packages. 

I didn't set out to write a tic tac toe program per se--I know there are simpler ways to do that!

# Installation
Clone this repository onto a system where Python is installed and the Python interpreter is available via the command line.

No dependencies beyond the Python standard library.

# Starting a game
Windows 10:
  
    $ python -m tictactoe
Linux:

    $ python3 -m tictactoe

# Playing a game
Enter moves as row, column coordinates in [0 .. 2] (integers between 0 and 2, inclusive). For example, (0,0) marks the top left corner square, (1,1) the center, and (2,0) the bottom left corner:

           col 0   col 1   col 2
    row 0  (0,0) | (0,1) | (0,2)
          ---------------------
    row 1  (1,0) | (1,1) | (1,2)
          ---------------------
    row 2  (2,0) | (2,1) | (2,2)
