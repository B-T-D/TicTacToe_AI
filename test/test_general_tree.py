import unittest

from tic_tac_toe.general_tree import GeneralTree

class TestNode(unittest.TestCase):
    """Tests for the _Node nested nonpublic class."""

    def test_init(self):
        """Confirm that a _Node object can be initialized."""
        test_node = GeneralTree._Node("Test element")
        self.assertIsInstance(test_node, GeneralTree._Node)

class TestPosition(unittest.TestCase):
    """Tests for the Position nested class."""

    def test_init(self):

if __name__ == '__main__':
    unittest.main()

