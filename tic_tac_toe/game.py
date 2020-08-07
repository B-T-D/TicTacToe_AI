"""Main game controller script."""

try:
    from tic_tac_toe.board import TicTacToeBoard
    from tic_tac_toe.commandline import CLIBoard
except:
    from board import TicTacToeBoard
    from commandline import CLIBoard

class Game:
    """Attributes and methods for running a game of Tic Tac Toe."""

    def __init__(self, player1=None, player2=None,
                 interface="commandline"):
        """

        Args:
            players (tuple): Two-element tuple of Player objects.
            interface (str): Interface type for the game.
        """
        self._player1 = Player(mover=True) # Internal convention that player1
        self._player2 = Player(mover=False) # moves first by definition.
        self._interface = interface
        if self._interface != "commandline":
            raise NotImplementedError

    def get_human_move_second(self):
        """Give human user the option of making the second move instead of
        the first."""
        return self._get_human_move_second_terminal()

    def _get_human_move_second_terminal(self):
        """Get command line input to determine if human player wants to move
        first or second (in a human vs. computer game)."""
        valid_input = False
        attempts = 0
        affirmative_raws = ['y', 'yes', '1', 'true', 't']
        negative_raws = ['n', 'no', '0', 'false', 'f']
        while (valid_input is False) and attempts < 3: # Just move on after 3 attempts
            print("Human player move second? (Y/N)")
            raw = input(">>>")
            try:
                if raw.lower() in affirmative_raws:
                    return True
                    valid_input = True
                elif raw.lower() in negative_raws:
                    return False
                    valid_input = True
            except ValueError:
                continue
            attempts += 1
        return False

    def _set_commandline_options(self):
        """Get command line inputs and update Player attributes as
        needed."""
        humans = self._get_human_players()
        self._get_player1_marker()
        if humans == 1: # != as XOR
            human_move_second = self._get_human_move_second_terminal()
            if human_move_second:
                self._player1._human = False
                self._player2._human = True
            else:
                self._player1._human = True
                self._player2._human = False
        elif humans == 2:
            self._player1._human = True
            self._player2._human = True
        elif humans == 0:
            self._player1._human = False
            self._player2._human = False

    def _get_human_players(self):
        """Get command line user input and return the number of human players
        in the game.

        Returns:
            (int): 0, 1, or 2.
        """
        valid_input = False
        while valid_input == False:
            print("Enter the number of human players (0, 1, or 2):")
            raw = input(">>>")
            try:
                if int(raw) in (0, 1, 2):
                    humans = int(raw)
                    valid_input = True
            except ValueError:
                continue
        return humans

    def _get_player1_marker(self):
        """Get command line user input to set the first-moving player's
        marker ('X' or 'O')."""
        mark = []
        valid_input = False
        while valid_input == False:
            print("Choose X or O for the first player (human's mark if human"
                  " vs. computer game) ('X' or 'O'):")
            raw = input(">>>")
            try:
                if raw.upper() in ('X', 'O'):
                    mark = raw.upper()
                    valid_input = True
            except ValueError:
                continue
        if mark == 'X':
            self._player1._marker = 1
            self._player2._marker = 2
        elif mark == 'O':
            self._player1._marker = 2
            self._player2._marker = 1

    def main(self): # todo arg parse and pass these at the command line
        if self._interface == "commandline":
            self._set_commandline_options()
        board = TicTacToeBoard(player=self._player1.int_marker())
        CLIBoard(board, self._player1, self._player2).main()

class Player:

    def __init__(self, human=True, marker=1, mover=True):
        """

        :param human (bool): True if player is human, False if computer
        :param mark (int): 1 for 'X', 2 for 'O'
        """
        self._human = human
        self._marker = marker
        self._mover = mover # Whether it's this player's turn.

    def marker(self):
        """Return string representation of the player's board marker."""
        if self._marker == 1:
            return "X"
        return "O"

    def is_human(self):
        """Return True if player is human, False if computer."""
        return self._human

    def int_marker(self):
        """Return integer representation of the player's board marker."""
        return self._marker

    def toggle_mover(self):
        """Toggle whether it's this player's turn, and return the player after
        toggling."""
        self._mover = not self._mover
        return self._mover

    def is_turn(self):
        """Return True if it's this player's turn to move, else False."""
        return self._mover

    def set_mover(self, value):
        """
        Set whether it's this player's turn.
        Args:
            value (bool): True if it's this player's turn, False if not.
        """
        self._mover = value

if __name__ == '__main__':
    Game().main()