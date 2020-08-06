try:
    from tic_tac_toe.board import TicTacToeBoard  # unittest defaults want it this way
    from tic_tac_toe.game_tree import GameTree
except:
    from board import TicTacToeBoard
    from game_tree import GameTree
    # to run the script from windows system command line

class CLIBoard:
    """Implements command line interface for the tic tac toe game."""

    def __init__(self, humans=2):
        self._board = TicTacToeBoard()

    def string_player(self, player: int) -> str:
        """Translate the player-code integer to a string showing its mark.
        Upper case 'X' if player is 1, upper case 'O' if 2."""
        if player == 1:
            return "X"
        return "O" # Trusting the caller completely, validation should've
                    #   been handled far upstream.

    def refresh_board(self):
        """Output the current boardstate to command line in a format that's
        useful for a human player."""
        print(self._board)
        print(f"\n    {self.string_player(self._board.player())}'s turn\n")

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

    def human_move(self):
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

    def computer_move(self):
        tree = GameTree()
        move = tree.optimal_move(self._board)
        self._board.mark(move[0], move[1])

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
            message = "Draw. No winner.\n" \
                      "https://en.wikipedia.org/wiki/Futile_game"
        print(f"{self._board}")
        print(message) 
        return message # for unittest expediency

    def player_v_player(self):
        """Main loop for a human vs. human game."""
        while self._board.winner() is None:
            self.refresh_board()
            self.human_move()
        self.handle_outcome()

    def player_v_computer(self):
        """Main loop for a human vs. computer game."""
        while self._board.winner() is None:
            self.refresh_board()
            self.human_move()
            self.refresh_board()
            if self._board.winner() is None: # Don't call computer_move() if human just ended the game.
                self.computer_move() # todo abstract to get player1_move() and get player2_move()
        self.handle_outcome()

    def computer_v_computer(self):
        """Main loop for a computer vs. computer game."""
        pass

    def main(self, player1, player2):
        """Main controlling loop for the game."""
        print("CLI.main() ran")
        print(player1.is_human() and player2.is_human())
        if (player1.is_human() and player2.is_human()):
            self.player_v_player()
        elif player1.is_human() != player2.is_human(): # != is XOR here. If one but not both are human.
            self.player_v_computer()

if __name__ == '__main__':
    CLIBoard.main()
