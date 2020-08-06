"""Tests for the GameTree._build_children and build_tree methods requiring multiple
complex-setUp test cases."""

import unittest

from tic_tac_toe.general_tree import LinkedQueue
from tic_tac_toe.game_tree import GameTree
from tic_tac_toe.board import TicTacToeBoard

class TestBuildForBlankRoot(unittest.TestCase):
    """Does the method build children correctly for a blank-board root?"""

    def setUp(self):
        self.tree = GameTree()
        self.tree._add_root(TicTacToeBoard()) # add blank tree at root

        # -------------- hard-coded correct child grids --------------------

        # First row
        child00 = TicTacToeBoard([
            [1,0,0],
            [0,0,0],
            [0,0,0]
        ])
        child01 = TicTacToeBoard([
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        child02 = TicTacToeBoard([
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0]
        ])

        # Second row
        child10 = TicTacToeBoard([
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0]
        ])
        child11 = TicTacToeBoard([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        child12 = TicTacToeBoard([
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 0]
        ])

        # Third row
        child20 = TicTacToeBoard([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0]
        ])
        child21 = TicTacToeBoard([
            [0, 0, 0],
            [0, 0, 0],
            [0, 1, 0]
        ])
        child22 = TicTacToeBoard([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 1]
        ])

        self.expected_children = [
            child00, child01, child02,
            child10, child11, child12,
            child20, child21, child22
        ]

        self.expected_children_grids = []

        for board in self.expected_children:
            self.expected_children_grids.append(board.board())


        assert len(self.expected_children) == 9


    def test_build_for_blank_root(self):
        """For a blank board root node, does the method build and enqueue the
        correct children?"""
        children_queue = LinkedQueue()
        self.tree._build_children(self.tree.root(), children_queue)

        self.assertEqual(9, len(children_queue))
        while not children_queue.is_empty():
            child = children_queue.dequeue()
            self.assertIn(child.element().board(), self.expected_children_grids)

    def test_build_full_game_tree(self):
        """Does _build_tree build the entire brute force tree of
        possible games when called on root?"""
        # todo broken and slow. Other things work, but initial version is
        #   returning more than the number of mathematically extant unique games
        #   (games meaning sequences of moves, not board configurations).
        self.fail("Takes too long with current bad algorithm.")
        self.tree._build_tree(self.tree.root())
        self.assertEqual(255168, len(self.tree))


class TestBuildLateGameSubtree(unittest.TestCase):
    """Test case where root is a late-game board object with few remaining possible
    children."""

    def setUp(self):
        self.tree = GameTree()
        grid = [
            [1,2,1],
            [1,2,2],
            [0,1,0]
        ]
        self.tree._add_root(TicTacToeBoard(grid=grid, player=2), move=(1,0)) # hasn't been scored yet
        self.child00 = TicTacToeBoard([
                [1, 2, 1],
                [1, 2, 2],
                [0, 1, 2]
            ])
        self.child01 = TicTacToeBoard([
            [1, 2, 1],
            [1, 2, 2],
            [2, 1, 0]
        ])
        self.child10 = TicTacToeBoard([
            [1, 2, 1],
            [1, 2, 2],
            [2, 1, 1]
        ])
        self.child11 = TicTacToeBoard([
            [1, 2, 1],
            [1, 2, 2],
            [1, 1, 2]
        ])


    def test_build_first_layer_children(self):
        """Does the method correctly build the two possible children?"""
        children_queue = LinkedQueue()
        self.expected_children_grids = [self.child00.board(),
                                        self.child01.board()]
        self.tree._build_children(self.tree.root(), children_queue)
        self.assertEqual(2, len(children_queue))
        while not children_queue.is_empty():
            child = children_queue.dequeue()
            self.assertIn(child.element().board(), self.expected_children_grids)

    def test_build_subtree(self):
        """Does the method correctly build the full subtree down to the
        gameover boards?"""
        self.tree._build_tree(self.tree.root())
        self.assertEqual(5, len(self.tree)) # Full subtree is 5 nodes

class BuildForLateGameSubtreeOneMovePrior(unittest.TestCase):
    """Construct tree for board with three moves remaining."""

    def setUp(self):
        self.tree = GameTree()
        grid = [
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 0]
        ]
        self.tree._add_root(TicTacToeBoard(grid)) # should be X's turn so default is right

    def test_build_full_tree(self):
        self.tree._build_tree(self.tree.root())
        self.assertEqual(14, len(self.tree)) # should be 15 nodes

class BuildForGameoverBoard(unittest.TestCase):

    def setUp(self):
        self.tree = GameTree()
        grid = [
            [1, 2, 0],
            [0, 1, 0],
            [0, 2, 1]
        ]

        self.tree._add_root(TicTacToeBoard(grid))

    def test_build_children_for_gameover(self):
        """Does the method return without enqueuing any children when called
        on a full-board?"""
        children_queue = LinkedQueue()
        self.tree._build_children(self.tree.root(), children_queue)
        self.assertTrue(children_queue.is_empty())




