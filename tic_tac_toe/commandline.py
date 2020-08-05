from tic_tac_toe.board import TicTacToeBoard

class CLIBoard:
    """Implements command line interface for the tic tac toe game."""

    def __init__(self):
        self._board = TicTacToeBoard()
        self._state = self._board.board()

    def _intboard_to_string(self):
        """Translate (0, 1, 2) notation to ('', 'X', 'O').

        Returns:
            (list): Array in which each element is either string '', string 'X',
                or string 'O'.
        """
        # Try to be smart about not calling these translator methods more often
        #   than is needed, would needlessly increase running time.
        #   If you wanted to eventually have arbitrarily large boards not just
        #   3 x 3, and this runs in O(n), where n is number of squares on the
        #   board, calling it too much could matter.
        
        stringboard = [[''] * 3 for i in range(3)] # 3 x 3 array initialized to
                                                    # all blank strings.

        for r in range(3):
            row = self._state[r]
            for col in range(3):
                if row[col] == 1:
                    stringboard[r][col] = 'X'
                elif row[col] == 2:
                    stringboard[r][col] = 'O'
                # implicit else just leave it as blank string
        return stringboard            

    def _stringboard_to_int(self):
        """Translate (None, 'X', 'O') notation to (0, 1, 2).

        Returns:
            (list): Array of ints each of which is either 0, 1, or 2.
        """
        pass
        # may never be needed if translating all updates to ternary notation
        #   right at the source rather than at the level of the whole board.

    def refresh_board(self):
        """Output the current boardstate to command line in a format that's
        useful for a human player."""
        print(f"{self._board.player()}'s turn")
        print(self._board)

    def get_mark_input(self):
        """Get player input of a location at which to place a new mark on the
        board.

        Returns:
            (tuple): (row, column) tuple of the location the player is attempting
                to place the mark.
        """
        print("Enter row and column to mark, format 'row, column':")
        raw = input(">>>")
        return raw

    def get_move(self):
        # While loop that continually prompts player for input until input is acceptable
        #   to Board.mark() method's validators
        row = None
        col = None
        valid_move = False
        while valid_move == False:
            raw = self.get_mark_input()
            for char in raw:
                if 48 <= ord(char) <= 50: # ascii for digit chars 0, 1, 2
                    if row is None:
                        row = ord(char) - 48
                    else:
                        col = ord(char) - 48
            # if the input is two ints, try submitting them
            if row is not None and col is not None:
                try:
                    self._board.mark(row, col)
                    valid_move = True
                except ValueError:
                    print("Invalid move position.")
                    row = None
                    col = None


    def send_move(self, coordinates: tuple):
        """Send row and colum of latest move to the board object to update
        the boardstate."""
        row, col = coordinates
        self._board.mark(row, col)

    def handle_outcome(self) -> str:
        """Output appropriate visual for win result.

        Args:
            outcome (int): 0 for draw, 1 for X win, 2 for O win.
        """
        if self._board.winner() == 1:
            message = "X wins!"
        elif self._board.winner() == 2:
            message = "O wins!"
        else:
            message = "Draw, no winner."
        print(message) 
        return message # for unittest expediency
        
    def main():
        """Main controlling loop for the game."""
        game = CLIBoard()
        while game._board.winner() is None:
            game.refresh_board()
            game.get_move()
        game.handle_outcome()
        # Detecting a draw might be best handled by the gametree. 

if __name__ == '__main__':
    CLIBoard.main()
