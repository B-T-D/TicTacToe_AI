# TicTacToe_AI
Plays tic tac toe using a game tree and minimax algorithm to find optimal moves. 

Includes a command line interface that supports human vs. computer, human vs. human, and computer vs. computer games. The AI should play a perfect game every time--always tie or win. 

# Installation
Clone this repository onto a system where Python is installed and the Python interpreter is available via the command line.

No dependencies beyond the Python standard library.

# Starting a game
Windows 10:
  
    $ python -m tictactoe
Linux:

    $ python3 -m tictactoe

# Playing a game
Enter moves as row, column integer coordinates between 0 and 2 inclusive. For example, (0,0) marks the top left corner square, (1,1) the center, and (2,0) the bottom left corner:

           col 0   col 1   col 2
    row 0  (0,0) | (0,1) | (0,2)
          ---------------------
    row 1  (1,0) | (1,1) | (1,2)
          ---------------------
    row 2  (2,0) | (2,1) | (2,2)
