import unittest

from tic_tac_toe.game_tree import GameTree
from tic_tac_toe.board import TicTacToeBoard

class TestAddOneChildToBlankBoard(unittest.TestCase):
    """Simple test case of adding a single child to an initially blank board.
    Not worried about adding all children, just confirming can add one as
    intended."""

    def setUp(self):
        self.tree = GameTree()
        self.tree._add_root(self, TicTacToeBoard()) # root is a blank board, player is X

    def placeholder(self):
        pass

class TestThreePositionTreeDrawWinLose(unittest.TestCase):
    # startint from same same as the test case used for biggest compute_score test
    """Test case for a starting board that has 6 moves on the board, X's move next,
     and remaining possible outcomes including all of win, loss, and draw."""

    pass