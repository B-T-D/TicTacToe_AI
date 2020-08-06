"""Main game controller script."""

try:
    from tic_tac_toe.board import TicTacToeBoard
    from tic_tac_toe.commandline import CLIBoard# unittest defaults want it this way
except:
    from board import TicTacToeBoard
    from commandline import CLIBoard # to run the script from windows system command line

class Game:
    """Attributes and methods for running a game of Tic Tac Toe."""

    def __init__(self, humans=1, interface="commandline"):
        """

        :param humans: Number of human players.
        :param interface: Interface type for the game.
        """
        self._humans = humans
        self._interface = interface
        if self._interface != "commandline":
            raise NotImplementedError

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
                  "vs. computer game) ('X' or 'O'):")
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
            intmark ==2
            othermark = 1
        if humans == 1:
            player1 = Player(human=True, mark=intmark)
            player2 = Player(human=False, mark=othermark)
        elif humans == 2:
            player1 = Player(human=True, mark=intmark)
            player2 = Player(human=True, mark=othermark)
        CLIBoard().main(player1, player2)

class Player:

    def __init__(self, human=True, mark=1):
        """

        :param human (bool): True if player is human, False if computer
        :param mark (int): 1 for 'X', 2 for 'O'
        """
        self._human = human
        self._mark = mark

    def mark(self):
        """Return string representation of the player's board marker."""
        if self._mark == 1:
            return "X"
        return "O"

    def is_human(self):
        """Return True if player is human, False if computer."""
        return self._human


if __name__ == '__main__':
    Game().main()