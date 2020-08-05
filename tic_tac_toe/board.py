class TicTacToeBoard:
    """Management of a Tic Tac Toe game (doesn't have a computer-player that
    does strategy against a human player).

    Board marks are represented as integers. 0 for a blank square, 1 for x,
    2 for O (to save small amount of memory, 28 bytes for the int vs 50 for
    a single-character string). 
    """

    def __init__(self, grid=None, player=1):
        """Start a new game. Allow caller to pass in an existing 3x3 grid
        representing an in-progress game. Allow caller to specify whether X or O is
        first-mover player, defaulting to X if not specified.

        Args:
            grid (list): 3 x 3 array of integers 0, 1, or 2.
        """
        if grid is not None:
            self._grid = grid # todo validate board
        else:
            self._grid = [[0] * 3 for j in range(3)] # 3 x 3 2D array of space character strings
            #   todo: Rename to "grid" or "squares"
        self._player = player
        # todo validate that player is either 1 or 2, fail immediately if player is e.g. 7

    def mark(self, row: int, col: int) -> None:
        """Put set value to 1 or 2 at position (row, col) for next player's turn.

        """
        # todo support callers passing a tuple
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise ValueError('Invalid board position')
        if self._grid[row][col] != 0: # if there's already a mark at that square
            raise ValueError('Board position occupied')
        if self.winner() is not None:
            raise ValueError('Game is already complete')
        self._grid[row][col] = self._player
        if self._player == 1: # swap the active player
            self._player = 2
        else:
            self._player = 1

    def _is_win(self, mark):
        """Check whether current board configuration is a win for the given
        player

        Args:
            mark (int): 1 for 'X' or 2 for 'O'

        Returns:
            (bool): True if current game board state is a win for the
                current player, else False.
        """

        board = self._grid # local variable for code compactness here
        # (authors are manually checking all 8 of the possible ways you could
        #   get three in a row--2 diagonals + 3 full-row + 3 full-column = 8.
        return (mark == board[0][0] == board[0][1] == board[0][2] or    # row 0
                mark == board[1][0] == board[1][1] == board[1][2] or    # row 1
                mark == board[2][0] == board[2][1] == board[2][2] or    # row 2
                mark == board[0][0] == board[1][0] == board[2][0] or    # column 0
                mark == board[0][1] == board[1][1] == board[2][1] or    # column 1
                mark == board[0][2] == board[1][2] == board[2][2] or    # column 2
                mark == board[0][0] == board[1][1] == board[2][2] or    # diagonal
                mark == board[0][2] == board[1][1] == board[2][0])      # rev diag

    def winner(self):
        """Return mark of winning player, 3 to indicate a tie, None to if
        game in progress."""
        for mark in [1, 2]:
            if self._is_win(mark):
                return mark
        if 0 not in self._grid[0]: # If no blank squares
            if 0 not in self._grid[1]: # Don't check more rows if already found a blank square
                if 0 not in self._grid[2]:
                    return 3
        return None

    def __str__(self):
        """Return string representation of the board in its current state."""
        rows = []
        for r in range(3):
            row = self._grid[r].copy()
            for i in range(3):
                if row[i] == 1:
                    row[i] = "X"
                elif row[i] == 2:
                    row[i] = "O"
                else:
                    row[i] = ''
            rows.append(row)
        colwidth = 5
        print_rows = []
        print_string = []
        for r in range(3):
            rowstring =\
                f"{rows[r][0]:^{colwidth}}|{rows[r][1]:^{colwidth}}|{rows[r][2]:^{colwidth}}"
            print_rows.append(rowstring)
        for string in print_rows:
            print_string.append(row)
        return '\n------------------\n'.join(print_rows)



    def board(self) -> list:
        """Public method to return the current board state as a 3 x 3 array.

        Returns:
            (list): 3 x 3 array representing current state of the tic tac toe board in
                0 / 1 / 2 notation convention.
        """
        return self._grid

    def player(self):
        """Public method to return the current player (whose turn it is).

        Returns:
            (int): 1 if it's X's turn to move, 2 if O's
        """
        return self._player

    def opponent(self):
        """Return non-mover opponent of the current player.

        Returns:
            (int): 1 if non-mover player is 'X', 2 if 'O'
        """
        return 2 if self.player() == 1 else 1
