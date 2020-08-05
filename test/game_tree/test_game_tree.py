import unittest

import copy

from tic_tac_toe.game_tree import GameTree
from tic_tac_toe.board import TicTacToeBoard

class TestGameTreeNode(unittest.TestCase):
    """
    Tests for GameTree's modified version of the _Node nested class
    it inherited from GeneralTree.
    """

    def setUp(self):
        blank_board = TicTacToeBoard().board()
        test_element = (blank_board, 0)
        self.test_node = GameTree._Node(test_element)

    def test_init(self):
        """Confirm that _Node object can be initialized."""
        self.assertIsInstance(self.test_node, GameTree._Node)

    def test_element_attribute(self):
        """Confirm that the element was initialized and can be accessed using
        the naming convention used in the parent, _element."""
        element = self.test_node._element
        expected_list = [[0,0,0],
                         [0,0,0],
                         [0,0,0]]
        expected_score = 0
        expected_element = (expected_list, expected_score)
        self.assertIsInstance(element, tuple)
        self.assertEqual(element, expected_element)

    def test_children_datatype(self):
        """Confirm that the children instance variable is a list."""
        self.assertIsInstance(self.test_node._children, list)

    def test_move_attribute(self):
        """Confirm that the _move attribute is accessible and was initialized
        to None."""
        self.assertIsNone(self.test_node._move)

    def test_score_attribute(self):
        """Confirm that the _score attribute is accessible and was initialized'
        to None."""
        self.assertIsNone(self.test_node._score)

    def test_non_none_move_attribute(self):
        """Can _Node._move value be set two a two-element tuple mimicking a
        (row, column) tuple, and then accessed?"""
        move = (0, 1)
        self.test_node._move = move
        self.assertEqual(move, self.test_node._move)

    def test_non_none_score_attribute(self):
        """Can _Node._score value be set to ints -1, 0, and 1?"""
        scores = [-1, 0, 1]
        for score in scores:
            self.test_node._score = score
            self.assertEqual(score, self.test_node._score)

class TestGameTreePosition(unittest.TestCase):
    """Tests for GameTree's modified version of the inherited Position
    nested subclass."""

    def setUp(self):
        self.test_element = TicTacToeBoard()
        self.node = GameTree._Node(self.test_element)
        container = [] # To pass to Position constructor (not normally called from outside the class)
        self.test_position = GameTree.Position(container, self.node)

    def test_init(self):
        """Confirm the object initialized and is of the expected type."""
        self.assertIsNotNone(self.test_position)
        self.assertIsInstance(self.test_position, GameTree.Position)

    def test_move(self):
        """Confirm Position.move() correctly returns underlying node's _move
        attribute."""
        move = (1, 0)
        self.test_position._node._move = move
        self.assertEqual(move, self.test_position.move())

    def test_score(self):
        """Confirm Position.score() correctly returns underlying node's _score
        attribute."""
        score = 1
        self.test_position._node._score = score
        self.assertEqual(score, self.test_position.score())

class TestAddRoot(unittest.TestCase):
    """Tests for GameTree's override of GeneralTree's _add_root() method to
    support adding move and score."""

    def setUp(self):
        self.tree = GameTree()

    def test_add_blank_board_root(self):
        """Does _add_root add a blank board whose underlying node has the
        expected attributes?"""
        blank_board = TicTacToeBoard()
        self.tree._add_root(blank_board)  # move and score default value of None is their correct value
        self.assertEqual(blank_board, self.tree.root().element())
        self.assertEqual(None, self.tree.root().move())
        self.assertEqual(None, self.tree.root().score())

    def test_add_first_move_board(self):
        """Does the function add a board with one move marked, and set
        the node's _move attribute accordingly?"""
        board = TicTacToeBoard()
        move = 1,1
        board.mark(move[0], move[1])
        self.tree._add_root(board, move)
        self.assertEqual(board, self.tree.root().element())
        self.assertEqual(None, self.tree.root().score())

    def test_add_gameover_board(self):
        """Does the function correctly handle a game-over board (a board whose
        score can be computed in isolation without looking at children)?"""
        grid = [
            [1,2,1],
            [0,2,2],
            [1,1,2]
        ] # add a board where x is one move away from winning
        board = TicTacToeBoard(grid)
        move = (1,0) # X's winning move in this example
        board.mark(move[0], move[1])
        assert board.winner() == 1
        assert board.player() == 2 # player should be set to O-2
        self.tree._add_root(board, move)
        score = self.tree.compute_score(self.tree.root())
        self.tree.root()._node._score = score
        self.assertEqual(-1, self.tree.root().score()) # minimax will return the flipped score,
                                                        # because there's no child.
                                                        # mark() call flipped the active player without adding a child.



class TestBuildLayer(unittest.TestCase):

    def setUp(self):
        self.full_board_1 = [[1, 1, 1,],
                            [1, 1, 1,],
                            [1, 1, 1]]
        self.tree = GameTree()
        self.tree._add_root((self.full_board_1, 0))

    def test_board_full(self):
        """Does the method do nothing when the board is already full?"""
        len_start = len(self.tree)
        self.tree._build_layer(self.tree.root(), player=1)
        self.assertEqual(len_start, len(self.tree))
        self.assertTrue(self.tree.is_leaf(self.tree.root()))


class TestBuildDumbTree(unittest.TestCase):
    """Tests for the method that builds a tree of all 250 possible legal
    board configurations."""

    def setUp(self):
        self.tree = GameTree()
        blank_board = TicTacToeBoard().board()
        self.tree._add_root((blank_board, 0))

        #self.tree.build_dumb_tree(self.tree.root(), player=1)

    def test_root_board(self):
        """Root's board should be blank."""
        expected = [[0,0,0],
                         [0,0,0],
                         [0,0,0]]
        actual = self.tree.root().element()[0]
        self.assertEqual(actual, expected)

    # def test_tree_size(self):
    #     """Are there 250 total positions in the tree?"""
    #     expected = 250
    #     actual = len(self.tree)
    #     self.assertEqual(expected, actual)

    # def testplaceholder(self):
    #     self.tree.parenthesize(self.tree.root())

class TestMiscSimpleMethods(unittest.TestCase):

    def setUp(self):
        self.tree = GameTree()

class TestAddUnmarkedChild(unittest.TestCase):
    """Tests for the method that adds a copy of the parent's board as a
    child."""

    def setUp(self):
        self.tree = GameTree()

class TestAddUnmarkedChildTwoMarksOnRoot(unittest.TestCase): # todo intended this to be a subclass of TestUnmarkedChild; unittest wouldn't run the nested tests
    """Case where position arg is root with in-progress marks on it
    and active player is 2."""

    def setUp(self):
        self.tree = GameTree()
        self.player = 2
        self.original_grid = [
            [1,0,1],
            [0,2,0],
            [0,0,0]
        ]
        self.grid = copy.deepcopy(self.original_grid)
        self.tree._add_root(TicTacToeBoard(grid=self.grid,
                                           player=self.player))
        self.child_0_0 = self.tree._add_unmarked_child(self.tree.root())

    def test_correct_grid_value(self):
        self.assertEqual(self.grid, self.child_0_0.element().board())

    def test_correct_player_value(self):
        self.assertEqual(self.player, self.child_0_0.element().player())

    def test_marking_child_grid_does_not_mark_parent_grid(self):
        """Does calling board's .mark() method on the child grid leave
        parent's grid unaffected?"""
        board_to_mark = self.child_0_0.element()
        board_to_mark.mark(0,1)
        expected_new_grid = [
            [1, 2, 1],
            [0, 2, 0],
            [0, 0, 0]
        ]
        self.assertEqual(self.original_grid, self.grid)
        self.assertEqual(expected_new_grid, self.child_0_0.element().board())



if __name__ == '__main__':
    unittest.main()

