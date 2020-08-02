class GeneralTree:
    """Concrete implementation of a general tree data structure. Intended to be
    reusable."""

    # ----------------------- nested nonpublic Node class --------------------

    class _Node:
        """Structure storing the underlying data and relevant links for
        use by the tree class's methods."""
        __slots__ = '_element', '_parent', '_children' # to make lighter in memory
        #   Will the _children thing work for an arbitrary number of children?

        def __init__(self, element, parent=None, children=None):
            """
            Args:
                element (object): Data of whatever type is to be stored in the
                    tree.
                parent (_Node): _Node object representing the parent 
                children (list): list containing other _Node objects
                
            Returns:
                None
            """
            self._element = element
            self._parent = parent
            self._children = children

    # ----------------------- nested Postiion class --------------------------

    # Public because we want the element() accessor method to be public, per
    #   the ADT. 

    class Position:
        """Abstraction representing the location of a single element."""
        pass

    # ----------------------- public accessor methods ------------------------

    def root(self):
        """
        Return Position representing the tree's root (or None if empty).

        Args:
            None

        Returns:
            (Position): Position object located at the root, or None if
                tree is empty.
        """
        pass

    def is_root(position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (bool): True if position is the root of the tree, else False.
        """
        pass

    def parent(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (Position): Position object that is position's parent, or None if
                position is the root of the tree.
        """
        pass

    def num_children(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (int): Number of chidren nodes of position.
        """
        pass

    def children(self, position):
        """Generate an iteration of Positions representing the children nodes
        of position.

        Args:
            position (Position): Position object located in this tree.

        Yields:
            (Position): The next Position object among position's children.
        """
        pass

    def is_leaf(self, position):
        """

        Args:
            position (Position): Position object located in this tree.

        Returns:
            (bool): True if position has no children, else False.
        """
        pass

    def __len__(self):
        """
        Returns:
            (int): Total number of Positions, i.e. elements, in the tree
        """
        pass

    def is_empty(self):
        """
        Returns:
            (bool): True if tree is empty, else False.
        """
        pass

    def positions(self):
        """
        Generate an iteration of all Positions of the tree. Order depends on
        traversal algorithm. 

        Args:
            None

        Yields:
            (Position): The next Postion object in the tree.
        """

    def __iter__(self):
        """
        Generate an iteration of the tree's elements (i.e. the underlying
        data, not their Positions).

        Yields:
            (object): The next object stored as an element of a tree Position.
                Of whatever type that data is.
        """
        pass
