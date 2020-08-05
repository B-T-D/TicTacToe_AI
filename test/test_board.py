import unittest

from tic_tac_toe.board import TicTacToeBoard

class TestBoardInit(unittest.TestCase):
    """Tests to confirm correct initialization of a Board object."""

    def test_init(self):
        """Test that the string representation of a blank board is a 2D array
        of 3 rows by 3 columns, with each element an int with value zero."""
        board = TicTacToeBoard()
        actual_boardstate = board._grid
        expected_boardstate = [[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]] 
        self.assertEqual(actual_boardstate, expected_boardstate)

    def test_init_existing_board(self):
        """Does the constructor accept an existing 3 x 3 grid and construct
        a board object with that instead of initializing a blank grid?"""
        in_progress = [
            [1, 2, 0],
            [0, 1, 0],
            [0, 2, 1]
        ]
        board = TicTacToeBoard(grid=in_progress)
        self.assertEqual(in_progress, board._grid)

class TestMark(unittest.TestCase):
    """Tests for the Board.mark() method."""

    def setUp(self):
        self.board = TicTacToeBoard()

    def test_mark_one(self):
        """Mark an X or O on the center square."""
        # Player should be 'X' after init, X moves first.
        self.board.mark(row=1, col=1)
        actual_boardstate = self.board._grid
        expected_boardstate = [[0, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]]
        self.assertEqual(actual_boardstate, expected_boardstate)
        self.assertEqual(self.board._player, 2) # player should've flipped

    def test_mark_two(self):
        """Mark an O as the second move."""
        self.board.mark(row=1, col=1)
        self.board.mark(row=0, col=0) # O attempts "fork" by playing in a corner
                                        # that has two potential win routes open
        actual_boardstate = self.board._grid
        expected_boardstate = [[2, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]]
        self.assertEqual(actual_boardstate, expected_boardstate)
        self.assertEqual(self.board._player, 1) # should be back to 1

    def test_invalid_board_position(self):
        """Confirm ValueError when attempting to mark at nonexistent grid
        coordinates."""
        with self.assertRaises(ValueError):
            self.board.mark(row=3, col=3)

    def test_board_position_occupied(self):
        self.board.mark(row=1, col=1) # X plays first at center
        with self.assertRaises(ValueError):
            self.board.mark(row=1, col=1) # attempt placing O at center

    def test_game_already_complete(self):
        """Confirm ValueError if one player has already won."""
        # Create simplified game-over board that wouldn't be legal in TTT rules
        gameover_board = TicTacToeBoard()
        gameover_board._grid = [[1, 0, 0],
                                [0, 1, 0],
                                [0, 0, 1]]
        assert gameover_board._is_win(1) == True # interrupt execution if _is_win
                                                # method not working, since
                                                # that's not what we're testing
        gameover_board._player = 2
        with self.assertRaises(ValueError):
            gameover_board.mark(row=1, col=2) # O marks in top right

class TestIsWin(unittest.TestCase):
    """Test all 8 possible winning configurations of the board."""

    def setUp(self):
        self.board = TicTacToeBoard()

    def test_illegal_wins(self):
        """Expedient tests for non-legal boardstates."""
        self.board._grid = [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]]
        p = 1 # shorthand for "player"
        for player in [1, 2]:
            p = player
            boardstates = { 
                'top_row': [[p, p, p],
                            [0, 0, 0],
                            [0, 0, 0]],
                'mid_row': [[0, 0, 0],
                            [p, p, p],
                            [0, 0, 0]],
                'btm_row': [[0, 0, 0],
                            [0, 0, 0],
                            [p, p, p]],
                'left_col': [[p, 0, 0],
                             [p, 0, 0],
                             [p, 0, 0]],
                'mid_col': [[0, p, 0],
                            [0, p, 0],
                            [0, p, 0]],
                'right_col': [[0, 0, p],
                              [0, 0, p],
                              [0, 0, p]],
                'diagonal': [[p, 0, 0],
                             [0, p, 0],
                             [0, 0, p]],
                'rev_diagonal': [[0, 0, p],
                                 [0, p, 0],
                                 [p, 0, 0]]
                }
            assert len(boardstates) == 8 # double check dict generated ok
            for win_state in boardstates:
                self.board._grid = boardstates[win_state]
                self.assertTrue(self.board._is_win(p))

class TestWinner(unittest.TestCase):
    """Tests for public winner() method."""

    def test_identify_draw(self):
        """Does the method return 3 to indicate a draw when called on
        TicTacToeBoard object with no winner and no remaining empty squares?"""
        grid = [
            [1,2,1],
            [1,2,2],
            [2,1,1]
        ]
        board = TicTacToeBoard(grid=grid)
        self.assertEqual(3, board.winner())

class TestBoard(unittest.TestCase):
    """Tests for the public get_board() method that returns the board to outside
    caller code."""

    def test_board(self):
        board = TicTacToeBoard().board()
        self.assertIsInstance(board, list)
        expected_list = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
        self.assertEqual(board, expected_list)

class TestSimpleMethods(unittest.TestCase):
    """Tests for simple methods that can share a single simple test case."""

    def setUp(self):
        grid = [
                [1, 2, 0],
                [0, 1, 0],
                [0, 2, 1]
            ]
        self.board = TicTacToeBoard(grid=grid)

    def test_str(self): # todo brittle
        """Tests for the __str__ method."""
        expected_string = "  X  |  O  |     \n------------------\n" \
                          "     |  X  |     \n------------------\n" \
                          "     |  O  |  X  "
        actual_string = str(self.board)
        self.assertEqual(expected_string, actual_string)

    def test_opponent(self):
        """Test the method that returns opponent of the current mover-player."""
        new_board = TicTacToeBoard()
        assert new_board.player() == 1 # should have instantiated with X as default first mover
        self.assertEqual(2, new_board.opponent())
        new_board.mark(2,0) # Send a move to the board to flip player
        self.assertEqual(1, new_board.opponent())

if __name__ == '__main__':
    unittest.main()
