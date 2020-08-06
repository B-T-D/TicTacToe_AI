"""Tests for the game controller script."""

import unittest

from tic_tac_toe.game import Game, Player

class TestInit(unittest.TestCase):
    """Confirm that a Game object can be instantiated."""

    def setUp(self):
        self.game = Game()

    def test_init(self):
        """Does the object exist and is it non-None?"""
        self.assertIsInstance(self.game, Game)
        self.assertIsNotNone(self.game)

    def test_raises_error_if_not_commandline(self):
        """Does __init__ raise error if interface argument is something other
        than command line?"""
        with self.assertRaises(NotImplementedError):
            Game(interface="GUI")


class TestPlayer(unittest.TestCase):
    """Simple tests for the Player class."""

    def test_toggle_mover(self):
        """Does the method invert the Player's mover value?"""
        player = Player()
        self.assertEqual(True, player.is_turn())
        returned = player.toggle_mover()
        self.assertFalse(returned)
        self.assertFalse(player.is_turn())

    def test_int_marker(self):
        """Does public int_marker() method return the correct integer
        representation of the player's marker?"""
        player = Player(marker=1)
        assert player.marker() == 'X'
        self.assertEqual(1, player.int_marker())
        player2 = Player(marker=2)
        print(player2._marker)
        assert player2.marker() == 'O'
        self.assertEqual(2, player2.int_marker())

    def test_is_turn(self):
        """Does is_turn() correctly return whether it's player's turn?"""
        player1 = Player()
        self.assertTrue(player1.is_turn())
        player1.toggle_mover()
        self.assertFalse(player1.is_turn())




