import unittest
import random

from tic_tac_toe.general_tree import GeneralTree

class TestNode(unittest.TestCase):
    """Tests for the _Node nested nonpublic class."""

    def setUp(self):
        self.test_node = GeneralTree._Node("Test element")

    def test_init(self):
        """Confirm that a _Node object can be initialized."""
        self.assertIsInstance(self.test_node, GeneralTree._Node)

    def test_children_datatype(self):
        """Confirm that the children instance variable is a list."""
        self.assertIsInstance(self.test_node._children, list)
        
class TestPosition(unittest.TestCase):
    """Tests for the Position nested class."""

    def setUp(self):
        self.test_element = "Test element"
        self.node = GeneralTree._Node(self.test_element)
        container = [] # Temporary. Just needs something to pass as container 
        self.test_position = GeneralTree.Position(container, self.node)

    def test_init(self):
        self.assertIsNotNone(self.test_position)
        self.assertIsInstance(self.test_position, GeneralTree.Position)

    def test_element(self):
        """Confirm that the element() method returns the test element's
        string data."""
        self.assertEqual(self.test_position.element(), "Test element")

    def test_eq(self):
        """Confirm that the __eq__ operator overloader method works as
        intended."""
        # create new position with object as its node:
        other_container = []
        new_position = GeneralTree.Position(other_container, self.node)
        self.assertEqual(self.test_position, new_position)

class TestTreeConstructors(unittest.TestCase):
    """Test __init__ and add_root."""

    def setUp(self):
        self.test_tree = GeneralTree()

    def test_init(self):
        self.assertIsInstance(self.test_tree, GeneralTree)
        self.assertIsNone(self.test_tree._root) # root should initialize to None
        self.assertEqual(self.test_tree._size, 0) # size should be zero

    def test_add_root(self):
        root = self.test_tree._add_root("Root element")
        self.assertEqual(self.test_tree._root, root._node)
        self.assertEqual(self.test_tree._size, 1)

class TestAddChild(unittest.TestCase):
    """Test _add_child internal method."""

    def setUp(self):
        self.test_tree = GeneralTree()
        self.root = self.test_tree._add_root("Root element")

    def test_add_one_child(self):
        """Confirm that a single child can be added."""
        child = self.test_tree._add_child(self.root, "First child element")
        self.assertEqual(self.test_tree._root._children,
                         [child._node])
                                    # root's _Node._children should now be a
                                    # a single-element list containing the
                                    # node object of the Position child

    def test_add_many_children(self):
        """Confirm that several children can be added with a shared parent."""
        expected_children_values = [1, 2, 3, 4, 5]
        for n in expected_children_values:
            self.test_tree._add_child(self.root, n)
        self.assertEqual(len(self.test_tree._root._children), 5)
        # Confirm the values of the underlying elements in the children list
        #   match the expected ones:
        for i in range(len(expected_children_values)):
            self.assertEqual(self.test_tree._root._children[i]._element,
                             expected_children_values[i])

class TestDelete(unittest.TestCase):
    """Tests for the _delete internal method."""

    def setUp(self):
        self.tree = GeneralTree()
        self.root = self.tree._add_root("Root element")
        # add one child
        self.first_child = self.tree._add_child(
            self.root, "First child element")

    def test_delete_one(self):
        """Test the simplest case of deleting a leaf that isn't the root."""
        self.tree._delete(self.first_child)
        self.assertEqual(self.tree._size, 1)

    def test_delete_node_with_exactly_one_child_leaf(self):
        """Test that when a node with exactly one child is deleted, that
        child is promoted to become the child of node that had been its
        grandparent."""
        grandchild = self.tree._add_child(self.first_child,
                                         "grandchild element")
        self.tree._delete(self.first_child)
        self.assertEqual(self.tree._size, 2) # Should be 2 nodes now
        self.assertEqual(grandchild._node._parent, self.root._node)

    def test_delete_node_with_exactly_one_nonleaf_child(self):
        """Does the 'promotion' still work correctly if the promoted node has
        multiple layers of its own children and grandchildren?"""
        random.seed(3)
        grandchild = self.tree._add_child(self.first_child,
                                         "grandchild element")
        # give grandchild multiple children
        great_grandchildren = [] # list to store these positions for later
        for i in range(5):
            ggc = self.tree._add_child(grandchild, i) # Element is just the int
            great_grandchildren.append(ggc)
        size_check = self.tree._size
        for ggc in great_grandchildren:
            randval = random.random() # Make some be leaves, others not
            if randval >= 0.5:
                for i in range(3):
                    self.tree._add_child(ggc, i)
        peak_size = self.tree._size
        assert self.tree._size == size_check + 9, f"size was {self.tree._size}"
        # with seed 3, should have added 3 (3 of the vals should've been over 0.5)
        #   Should have added 9 total, 3 * 3.
        self.tree._delete(self.first_child)
        self.assertEqual(self.tree._size, peak_size - 1) # Should only have
                                                        # decreased by 1
        self.assertEqual(grandchild._node._parent, self.root._node)
        for ggc in great_grandchildren: # all greatgrandchildren should have same
                                        #   parent they started with.
            self.assertEqual(ggc._node._parent, grandchild._node)
        
        
        
            

class TestPublicAccessors(unittest.TestCase):
    """Test that the main public accessor methods work for a simple test
    tree with 3 layers.
    """

    def setUp(self):
        self.tree = GeneralTree()
        # Create a 4-layer tree with non-uniform numbers of children. 4th layer
        #   is a single element, all other children of depth 3 are leaves.

        
        
        
        
        

if __name__ == '__main__':
    unittest.main()

