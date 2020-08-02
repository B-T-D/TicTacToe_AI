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

    def test_delete_node_with_multiple_children(self):
        """Does the _delete method raise ValueError when attempting to delete
        a node whose Position has more than one child?"""
        for i in range(3):
            self.tree._add_child(self.first_child, i)
        assert self.tree.num_children(self.first_child) == 3
        with self.assertRaises(ValueError):
            self.tree._delete(self.first_child)
        
class TestPublicAccessors(unittest.TestCase):
    """Test that the main public accessor methods work for a simple test
    tree with 3 layers.
    """

    def setUp(self):
        self.tree = GeneralTree()
        # Create a 4-layer tree with non-uniform numbers of children. 4th layer
        #   is a single element, all other children of depth 3 are leaves.
        self.root = self.tree._add_root("Root element")
        self.first_child = self.tree._add_child(self.root,
                                                "First child element")

    def test_root(self):
        """Does root() return a Position referencing the same node as
        the tree's root?"""
        self.assertEqual(self.tree.root(),
                         self.tree._make_position(self.tree._root))

    def test_is_root(self):
        """Does is_root() correctly return True when called on a Position
        that is root, and false when called on a Position that is not root?"""
        self.assertTrue(self.tree.is_root(self.root))
        self.assertFalse(self.tree.is_root(self.first_child))

    def test_parent(self):
        """Does parent() correctly return the Position object corresponding to
        the parent node of arg position when position is not root, and None
        when called on a Position that is root?"""
        self.assertEqual(self.tree.parent(self.first_child), self.root)
        self.assertIsNone(self.tree.parent(self.root))

    def test_is_leaf(self):
        """Does is_leaf() correctly return True when called on a position that
        has no children, and False when called on a position that has at least
        one child?"""
        self.assertTrue(self.tree.is_leaf(self.first_child))
        self.assertFalse(self.tree.is_leaf(self.root))

    def test_len(self):
        """Obvious-case tests for len(tree) where the method is being called
        in isolation, not used in combination with anything else."""
        # len() should be 2 with the 2 elements added to self.tree by setUp
        self.assertEqual(len(self.tree), 2)
        # len of a new tree should be 0
        new_tree = GeneralTree()
        self.assertEqual(len(new_tree), 0)
        # Add root and 5 children of root, len should be 6
        new_tree._add_root("NT root element")
        for i in range(5):
            new_tree._add_child(new_tree.root(), i)
        self.assertEqual(len(new_tree), 6)
        # Add 10 children to each of those children, len should be 56
        for child in new_tree.root()._node._children: # todo (the GeneralTree.children() iterator isn't implemented yet)
            child = new_tree._make_position(child)
            for i in range(10):
                latest_child = new_tree._add_child(child, i) # For expediency
                                                            # in using one leaf
                                                            # below
        self.assertEqual(len(new_tree), 56)
        # Confirm the _delete method decrements length
        prior_length = len(new_tree)
        new_tree._delete(latest_child)
        self.assertEqual(len(new_tree), prior_length - 1)

    def test_is_empty(self):
        """Does is_empty() return True if tree is empty, False if not?"""
        self.assertFalse(self.tree.is_empty())
        # Try it on a tree that was nonempty, then was emptied out:
        self.tree._delete(self.first_child)
        self.tree._delete(self.root)
        self.assertTrue(self.tree.is_empty())
        # Try it on a new blank tree:
        new_tree = GeneralTree()
        self.assertTrue(new_tree.is_empty())

class TestNonpublicTraversalMethods(unittest.TestCase):
    """Tests for the nonpublic tree-traversal methods used by the various public
    generators."""

    pass

class TestPublicGenerators(unittest.TestCase):
    """Tests for the public methods that generate an iteration."""

    def setUp(self):
        # Build 12-element test tree
        self.tree = GeneralTree()
        self.tree._add_root(1)
        for i in range(2, 5): # Children of root with elements 2, 3, 4
            self.tree._add_child(self.tree.root(), i)

        # 2 has one leaf-child with element=5
        node_2 = self.tree.root()._node._children[0]
        assert node_2._element == 2 # double check correct node, this isn't an
                                    #   ordered tree, so relying on list's
                                    #   ordering to access a specific node for now
        self.tree._add_child(self.tree._make_position(node_2), 5)

        # 3 has 4 children, 6, 7, 8, and 9
        node_3 = self.tree.root()._node._children[1]
        assert node_3._element == 3
        for i in range(6, 10):
            self.tree._add_child(self.tree._make_position(node_3), i)
        # Among 3's children, 6 has one child, 12; other 3 are leaves
        node_6 = node_3._children[0]
        assert node_6._element == 6
        self.tree._add_child(self.tree._make_position(node_6), 12)

        # Node 4 has two children, 10 and 11, both leaves
        node_4 = self.tree.root()._node._children[2]
        assert node_4._element == 4
        for i in range(10, 12):
            self.tree._add_child(self.tree._make_position(node_4), i)
        assert len(self.tree) == 12 # confirm all 12 elements in the tree

    def test_children(self):
        """Does the children() method allow caller to iterate over the Positions
        that represent the children of the Position the method was called with?
        """
        expected_root_children_elements = set([2, 3, 4]) # Values stored at root's
                                                        # children
        actual_root_children_elements = []
        for child in self.tree.children(self.tree.root()):
            actual_root_children_elements.append(child._node._element)
        actual_root_children_elements = set(actual_root_children_elements)
        self.assertEqual(actual_root_children_elements,
                         expected_root_children_elements)
        
        
        


if __name__ == '__main__':
    unittest.main()

