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

class TestPossibleMoves(unittest.TestCase):
    """Tests for the method that returns all possible move coordinates for
    a given position."""

    def setUp(self):
        self.tree = GameTree()


    def test_blank_board(self):
        """Does the method return a queue of 9 tuples, representing all squares
        on the board, when input is a blank board?"""
        self.tree._add_root(TicTacToeBoard())
        moves_list = self.tree._possible_moves(self.tree.root())
        self.assertEqual(9, len(moves_list))
        # construct set of all squares in the board:
        expected_moves_set = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
                              (2, 0), (2, 1), (2, 2)}
        moves_set = set(moves_list)
        self.assertEqual(expected_moves_set, moves_set) # confirm all squares in set

    def test_three_blank_squares(self):
        """Does the method correctly return a queue containing the three
        remaining blank squares in a late-game board?"""
        grid = [
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 0]
        ]
        self.tree._add_root(TicTacToeBoard(grid))
        moves_list = self.tree._possible_moves(self.tree.root())
        self.assertEqual(3, len(moves_list))
        expected_moves_set = {(1,0), (2,0), (2,2)}
        moves_set = set(moves_list)
        self.assertEqual(expected_moves_set, moves_set)


class TestScoreLeaf(unittest.TestCase):
    """Simple test cases for the method that non-recursively returns a leaf's
    score."""

    def setUp(self):
        self.tree = GameTree()

    def test_correct_score_win(self):
        """Does the method return 1 when position's element is a board where
        player won?"""
        grid = [
            [1, 2, 1],
            [0, 2, 2],
            [1, 1, 1]
        ]
        self.tree._add_root(TicTacToeBoard(grid))
        self.tree.root()._node._move = (2,0) # Value of move if X had just won.
        score = self.tree._score_leaf(self.tree.root())
        expected_score = 1
        self.assertEqual(expected_score, score)
        self.assertEqual(expected_score, self.tree.root().score())

    def test_correct_score_loss(self):
        """Does the method return -1 when position's element is a board where
        player lost?"""
        grid = [
            [1, 2, 1],
            [2, 2, 2],
            [0, 1, 1]
        ]
        self.tree._add_root(TicTacToeBoard(grid))
        self.tree.root()._node._move = (1, 0)  # Value of move if O had just won (moving illegally on X's turn)
        score = self.tree._score_leaf(self.tree.root())
        expected_score = -1
        self.assertEqual(expected_score, score)
        self.assertEqual(expected_score, self.tree.root().score())

    def test_correct_score_draw(self):
        """Does the method return 0 when position's element is a board ending
        in a draw?"""
        draw_grid = [
            [1, 2, 1],
            [1, 2, 2],
            [2, 1, 1]
        ]
        self.tree._add_root(TicTacToeBoard(draw_grid))
        self.tree.root()._node._move = (
        1, 0)  # Pretend X just moved here, O magically moved at (2,0) simultaneously
        score = self.tree._score_leaf(self.tree.root())
        expected_score = 0
        self.assertEqual(expected_score, score)
        self.assertEqual(expected_score, self.tree.root().score())

    def test_non_leaf_raises_error(self):
        self.tree._add_root(TicTacToeBoard([
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 1]
        ]))
        child = self.tree._add_marked_child(self.tree.root(), move=(2,0))
        with self.assertRaises(ValueError):
            self.tree._score_leaf(self.tree.root())

    def test_uses_parent_player_value(self):
        """When top level player value is different than leaf's (i.e. one
        has odd depth, other even), does the method use the top level value?"""
        self.tree._add_root(TicTacToeBoard([
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 1]
        ]))
        child = self.tree._add_marked_child(self.tree.root(), move=(2, 0))
        assert self.tree.root().element().player() == 1
        assert child.element().player() == 2
        assert child.element().winner() == 1
        child._node._score = None # cancel whatever _add_marked_child did
        assert child.score() is None, f"child.score() = {child.score()}"
        expected_score = 1 # X win should count as a +1 since top level player is X
        score = self.tree._score_leaf(child)
        self.assertEqual(expected_score, score)
        self.assertEqual(expected_score, child.score())

class TestScoreSubtree(unittest.TestCase):
    """Simple testcases for _score_subtree, not necessarily representing
    legally reachable boardstates."""

    def setUp(self):
        self.tree = GameTree()

    def test_score_parent_of_leaves(self):
        """If all of subtree root's children are base-case leaves, does the
        method correctly score those leaves and set parent's score to the max?"""
        start_grid = [
            [1,2,1],
            [0,2,2],
            [0,1,1]
        ]
        self.tree._add_root(TicTacToeBoard(start_grid))
        X_win_grid = [
            [1, 2, 1],
            [0, 2, 2],
            [1, 1, 1]
        ]
        X_win_child = self.tree._add_child(self.tree.root(), TicTacToeBoard(X_win_grid))
        X_win_child._node._move = (2,0)

        O_win_grid = [
            [1, 2, 1],
            [2, 2, 2],
            [0, 1, 1]
        ]
        O_win_child = self.tree._add_child(self.tree.root(), TicTacToeBoard(O_win_grid))
        O_win_child._node._move = (1,0)

        draw_grid = [
            [1, 2, 1],
            [1, 2, 2],
            [2, 1, 1]
        ]
        draw_child = self.tree._add_child(self.tree.root(), TicTacToeBoard(draw_grid))
        draw_child._node._move = (1,0) # Really there were two moves, setting it to what would've been an X move that caused a draw

        assert len(self.tree) == 4

        score = self.tree._score_subtree(self.tree.root())
        self.assertEqual(1, score) # should take the X win child's score

class TestSubtreeOptimalMove(unittest.TestCase):
    """Simple setUp tests for internal method that returns the optimal move
    for a given position's boardstate."""

    def setUp(self):
        self.tree = GameTree()

    def test_obvious_win_move_X(self):
        """Does the method return correct coordinates for input boardstate
        where the mover player can win on the next move?"""
        grid = [
            [0, 2, 1],
            [0, 2, 2],
            [0, 1, 1]
        ]
        self.tree._add_root(TicTacToeBoard(grid))
        assert self.tree.root().element().player() == 1,\
            f"player = {self.tree.root().element().player()}"
        expected_move = (2,0)
        move = self.tree._subtree_optimal_move(self.tree.root())
        self.assertEqual(expected_move, move)

    def test_obvious_win_move_O(self):
        """Does the method return correct winning move coordinates for input
        boardsate where mover player is 'O' and can win in next move?"""
        grid = [
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 1]
        ]
        self.tree._add_root(TicTacToeBoard(grid, player=2))
        assert self.tree.root().element().player() == 2, \
            f"player = {self.tree.root().element().player()}"
        expected_move = (1,0) # O should play at 1,0 and win.
        move = self.tree._subtree_optimal_move(self.tree.root())
        self.assertEqual(expected_move, move)

    def test_choose_draw_over_loss(self):
        """Given boardstate where one available move will lead to draw, the other
        to loss, does the method return the move that leads to draw?"""
        pass

class TestOptimalMove(unittest.TestCase):
    """Simple setUp tests for the public method that takes TicTacToeBoard as
    its input and returns the active player's optimal move."""

    def setUp(self):

        self.dummy_tree = GameTree() # instance to enable calling the method

    def test_obvious_win_move_X(self):
        grid = [
            [0, 2, 1],
            [0, 2, 2],
            [0, 1, 1]
        ]

        board = TicTacToeBoard(grid)
        expected_move = (2,0)
        move = self.dummy_tree.optimal_move(board)
        self.assertEqual(expected_move, move)

    def test_obvious_win_move_O(self):
        """Does the method return correct winning move coordinates for input
        boardsate where mover player is 'O' and can win in next move?"""
        grid = [
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 1]
        ]
        board = TicTacToeBoard(grid, player=2)
        expected_move = (1, 0)
        move = self.dummy_tree.optimal_move(board)
        self.assertEqual(expected_move, move)

    def test_optimal_first_move_X(self):
        """Does the method return the correct optimal opening move for X?"""
        tree = GameTree() # need a fresh tree
        board = TicTacToeBoard() # blank board with player X
        expected_moves = [(0, 0), (0, 2), (2, 0), (2, 2)] # one of the corners
        move = tree.optimal_move(board)
        self.assertIn(move, expected_moves)

if __name__ == '__main__':
    unittest.main()

