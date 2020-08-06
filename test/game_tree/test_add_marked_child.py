import unittest

from tic_tac_toe.game_tree import GameTree
from tic_tac_toe.board import TicTacToeBoard

# todo prob doesn't need to be its own module

class TestAddOneChildToBlankBoard(unittest.TestCase):
    """Simple test case of adding a single child to an initially blank board.
    Not worried about adding all children, just confirming can add one as
    intended."""

    def setUp(self):
        self.tree = GameTree()
        self.tree._add_root(TicTacToeBoard()) # root is a blank board, player is X
        self.move = (1,1) # First mark in the center square.

    def test_add_correct_element(self):
        child = self.tree._add_marked_child(self.tree.root(), move=self.move)
        grid = [
            [0,0,0],
            [0,1,0],
            [0,0,0]
        ]
        expected_element = TicTacToeBoard(grid, player=2)
        self.assertEqual(expected_element.board(), child.element().board())
            # The grids are identical, the TicTacToeBoard objects are not--that's
            #   the point of the deepcopy.

class TestThreePositionTreeDrawWinLose(unittest.TestCase):
    # startint from same same as the test case used for biggest compute_score test
    """Test case for a starting board that has 6 moves on the board, X's move next,
     and remaining possible outcomes including all of win, loss, and draw."""

    pass