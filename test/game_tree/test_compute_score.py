import unittest

from tic_tac_toe.game_tree import GameTree
from tic_tac_toe.board import TicTacToeBoard

import copy



class TestSinglePositionTreeXWin(unittest.TestCase):
    """"Test case where tree is a single Position, whose element is
    a game-over boardstate where X won."""

    def setUp(self):
        self.tree = GameTree()
        self.board = TicTacToeBoard()

        # Build the winning board using the board object's methods, not by
        #   directly manipulating the array or a mockup 3 x 3 array:

        end_board = [
            [1, 2, 0],
            [0, 1, 0],
            [0, 2, 1]
        ] # x wins diagononally in as few moves as possible

        self.board.mark(0,0)
        self.board.mark(2,1)
        self.board.mark(1,1)
        self.board.mark(0,1)
        self.board.mark(2,2)

        assert self.board._grid == end_board
        assert self.board.winner() == 1

        # Make a root in self.tree with self.board as its element
        self.tree._add_root(self.board)

    def test_score_is_neg1(self):
        """Does the function return 1 for a board at a root-and-leaf position
        where 1 is the winner?"""

        assert self.board.player() == 2 # Should be at 2 since X made the final
                                        # (and winning) move in setUp's mark() calls
        self.assertEqual(-1, self.tree.compute_score(self.tree.root()))

class TestSinglePositionTreeOWin(unittest.TestCase):
    """Test case where tree is a single Position, whose element is a game-over
    board state where 'O' won."""

    def setUp(self):
        self.tree = GameTree()
        self.board = TicTacToeBoard(player=2)

        # Build the winning board using the board object's methods, not by
        #   directly manipulating the array or a mockup 3 x 3 array:

        end_board = [
            [2, 1, 0],
            [0, 2, 0],
            [0, 1, 2]
        ] # x wins diagononally in as few moves as possible

        self.board.mark(0,0)
        self.board.mark(2,1)
        self.board.mark(1,1)
        self.board.mark(0,1)
        self.board.mark(2,2)

        assert self.board._grid == end_board
        assert self.board.winner() == 2

        # Make a root in self.tree with self.board as its element
        self.tree._add_root(self.board)

    def test_score_is_neg1(self):
        """Does the function return 1 for a board at a root-and-leaf position
        where 1 is the winner?"""

        assert self.board.player() == 1 # Should be at 2 since X made the final
                                        # (and winning) move in setUp's mark() calls
        self.assertEqual(-1, self.tree.compute_score(self.tree.root()))

class TestThreePositionTreeDrawWinLose(unittest.TestCase):
    """Test case for a three position subtree where root is an incomplete board
    with three children, one representing a draw, one representing an X win,
    and one representing an O win."""
    # Not concernet with these being legally-reachable boardstates (they
    # couldn't all exist on the same level like this in a real game). Goal is
    # just to unit test that the function assigns 1 vs -1 vs 0 correctly at
    # a given level (a constant value for player).
    # Constructing them with manual assignments to board's internal instance variables,
    #   not using the public mark() method.

    def setUp(self):
        self.tree = GameTree()
        X_win = [
            [1,2,0],
            [0,1,0],
            [0,2,1]
        ]
        O_win = [
            [0,1,2],
            [1,2,0],
            [2,1,0]
        ]
        draw = [
            [1,2,1],
            [2,2,1],
            [1,1,2]
        ]

        player = 1

        X_win_board = TicTacToeBoard(player)
        O_win_board = TicTacToeBoard(player)
        draw_board = TicTacToeBoard(player)

        X_win_board._grid = X_win
        assert X_win_board.winner() == 1
        O_win_board._grid = O_win
        assert O_win_board.winner() == 2
        draw_board._grid = draw
        assert draw_board.winner() == 3

        # make a root with a blank board
        self.tree._add_root(TicTacToeBoard(player=2)) # opposite of ._player on the child boards

        # Add child for each of the result boards
        self.X_win_position = self.tree._add_child(self.tree.root(), X_win_board)
        self.O_win_position = self.tree._add_child(self.tree.root(), O_win_board)
        self.draw_position = self.tree._add_child(self.tree.root(), draw_board)

        assert len(self.tree) == 4
        assert self.tree.num_children(self.tree.root()) == 3

    def test_X_win_scores_poz1(self):
        self.assertEqual(1, self.tree.compute_score(self.X_win_position))

    def test_O_win_scores_neg1(self):
        """Does the score function return -1 for the position where O wins?"""
        self.assertEqual(-1, self.tree.compute_score(self.O_win_position))

    def test_draw_scores_zero(self):
        """Does the score function return 0 for a draw?"""
        self.assertEqual(0, self.tree.compute_score(self.draw_position))


class TestMultiLayerTree(unittest.TestCase):
    """Tests for a three-layer subtree starting with root as a late game with
    7 marks on board and remaining possible outcomes X win and draw."""

    def setUp(self):
        self.tree = GameTree()
        self.board = TicTacToeBoard()
        assert self.board.player() == 1

        # Make the root board using move() method.
        self.board.mark(0,0) # X moves first into corner
        self.board.mark(1,1)
        self.board.mark(0,2)
        self.board.mark(0,1) # O blocks
        self.board.mark(2,1)
        self.board.mark(1,2) # O makes two in a row in middle row
        self.board.mark(1,0) # X blocks. This is now root for this test

        self.tree._add_root(self.board)  # Putting in entire board object as the element,
                                        #   i.e. it'll include the _player attribute

        # add a depth=1 child where O marks in the bottom right corner
        self.child_0_0 = self.tree._add_unmarked_child(self.tree.root())
        self.child_0_0.element().mark(2,2) # send O's mark
        # add that child's sole possible child--board where x plays in the last
        #   remaining blank square and wins.
        self.child_1_0 = self.tree._add_unmarked_child(self.child_0_0)
        self.child_1_0.element().mark(2,0) # send X's mark
        assert self.child_1_0.element().winner() == 1 # confirm X won.

        # add second depth=1 child where O marks in the bottom left corner
        self.child_0_1 = self.tree._add_unmarked_child(self.tree.root())
        self.child_0_1.element().mark(2,0)
        # add this child's sole possible child at depth=2--board where X plays
        #   in the last blank square and causes a draw.
        self.child_1_1 = self.tree._add_unmarked_child(self.child_0_1)
        self.child_1_1.element().mark(2,2) # send X's mark.
        assert self.child_1_1.element().winner() == 3, f"winner is {self.child_1_1.element().winner()}"

        # Tree should now be 5 positions total
        assert len(self.tree) == 5

    def test_basecase_leaves(self):
        """Does the function return the correct scores for the leaf nodes
        of this subtree--the base case of the recursion?"""
        # the one where X won should return -1 since O lost and X's .mark()
        #   call set ._player to 'O'
        self.assertEqual(-1, self.tree.compute_score(self.child_1_0))
        # Leaf with draw should score zero
        self.assertEqual(0, self.tree.compute_score(self.child_1_1))

    def test_height_1_subtree_root(self):
        """For a position with one nonzero-scoring child, does the function
        return the negation of that child's score?"""
        # Position with player=X whose child represents the sole remaining
        #   possible move being an X win should score 1.
        assert self.tree.depth(self.child_0_0) == 1
        # at child 0_0, player is O-2. Minimax should be returning the "max"
        #   of the children, which means -1 because there's only one child.
        self.assertEqual(-1, self.tree.compute_score(self.child_0_0))

    def test_height_2_subtree_root(self):
        """Does a root with 2 layers beneath it, with multiple diverging
        values to "choose from", correctly return the max to its caller?"""
        # Player should be O-2 at root. Root represents a boardstate where
        #   it would be O's turn. O would be calling minimax to identify the
        #   max scoring move option.
        assert self.tree.root().element().player() == 2
        # Max should be 0 -- only possible outcomes are draw and X win.
        self.assertEqual(0, self.tree.compute_score(self.tree.root()))

class TestHeight4Subtree(unittest.TestCase):
    """Test case with root one move earlier than previous. A height-4 subtree,
    where root is a board with three blank squares remaining, X's move."""

    def setUp(self):
        self.tree = GameTree()
        self.grid = [
            [1, 2, 1],
            [0, 2, 2],
            [0, 1, 0]
        ]


    def test_score_grid(self):
        """Does compute_score() return zero for root's score?"""
        self.tree._add_root(TicTacToeBoard(self.grid))
        self.assertEqual(0, self.tree.compute_score(self.tree.root()))

    def test_score_subtree(self):
        """Does the score subtree method set root's score to its intended
         minimax value of zero, after the full subtree is constructed?"""
        self.tree._add_root(TicTacToeBoard(self.grid))
        self.tree._build_tree(self.tree.root())
        print(f"root's score {self.tree.root()._node._score}")
        print(f" root().score() is None: {self.tree.root().score() is None}")
        assert len(self.tree) == 14 # should be 14 total positions now
        assert self.tree.root().element().player() == 1
        score = self.tree._score_subtree(self.tree.root())
        for child in self.tree.children(self.tree.root()):
            print(f"child is \n{child.element()}")
            print(f"child's score is {child.score()}")
        self.assertEqual(0, score)

    def test_subtree_optimal_move_player_X(self):
        """Does internal optimal move method return the correct next move for
        each position in the tree, where computer is moving for X?"""
        self.tree._add_root(TicTacToeBoard(self.grid))
        expected_move = (1,0) # The only move that leads to a draw for X on the recurring example subtree.
        board = self.tree.root().element() # unpack for cleaner .mark() calls
        move = self.tree._subtree_optimal_move(self.tree.root())
        self.assertEqual(expected_move, move)
        board.mark(move[0], move[1])

        # O's turn. O should mark at (2,0), else X wins next turn.
        print(f"-----------------{len(self.tree)}----------------------")
        grid = copy.deepcopy(board.board())
        # Current approach is to construct entirely new GameTree for each move.
        tree = GameTree()
        tree._add_root(TicTacToeBoard(grid, player = 2))
        board = tree.root().element()
        assert board.player() == 2
        print(f"board is now\n{board}")
        expected_move = (2,0)
        move = tree._subtree_optimal_move(tree.root())
        self.assertEqual(expected_move, move)
        board.mark(move[0], move[1])

    def test_optimal_move_through_gameover(self):
        """Starting with this test case's grid, does optimal_move() return
        the correct moves for each player?"""
        board = TicTacToeBoard(self.grid)

        # X's turn. Move should be (1,0).
        expected_move = (1, 0)
        move = self.tree.optimal_move(board)
        self.assertEqual(expected_move, move)
        board.mark(move[0], move[1]) # Mark this same board object, future subtrees will generate from its future states.

        # O's turn. Move should be (2,0).
        new_tree = GameTree()
        expected_move = (2, 0)
        move = new_tree.optimal_move(board)
        self.assertEqual(expected_move, move)
        board.mark(move[0], move[1])




if __name__ == '__main__':
    unittest.main()