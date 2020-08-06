"""Main game controller script."""

try:
    from tic_tac_toe.board import TicTacToeBoard
    from tic_tac_toe.commandline import CLIBoard # unittest defaults want it this way
except:
    from board import TicTacToeBoard
    from commandline import CLIBoard # to run the script from windows system command line

class Game:
    """Attributes and methods for running a game of Tic Tac Toe."""

    def __init__(self, players=None, interface="commandline"):
        """

        Args:
            players (tuple): Two-element tuple of Player objects.
            interface (str): Interface type for the game.
        """
        self._players = players
        self._interface = interface
        if self._interface != "commandline":
            raise NotImplementedError

    def _validate_mover_status(self, players):
        """
        If both players have same mover attribute, reset player1 to be mover.
        If it's neither of their turn or both of their turn, set it to player1
        turn.
        Args:
            players (list): This Game's _players attribute.
        :return:
        """
        player1 = players[0]
        player2 = players[1]
        if player1.is_turn() == player2.is_turn():
            player1.set_mover(True)
            player2.set_mover(False)


    def main(self): # todo arg parse and pass these at the command line
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
        mark = []
        othermark = None
        intmark = None
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
            intmark = 1
            othermark = 2
        elif mark == 'O':
            intmark = 2
            othermark = 1
        if humans == 1:
            player1 = Player(human=True, marker=intmark, mover=True)
            player2 = Player(human=False, marker=othermark, mover=False)
        elif humans == 2:
            player1 = Player(human=True, marker=intmark, mover=True)
            player2 = Player(human=True, marker=othermark, mover=False)
        elif humans == 0:
            player1 = Player(human=False, marker=intmark, mover=True)
            player2 = Player(human=False, marker=othermark, mover=False)
        board = TicTacToeBoard(player=player1.int_marker())
        CLIBoard(board, player1, player2).main()

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