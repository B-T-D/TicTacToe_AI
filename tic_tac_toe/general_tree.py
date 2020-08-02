class GeneralTree:
    """Concrete implementation of a general tree data structure. Intended to be
    reusable."""

    # ----------------------- nested nonpublic Node class --------------------

    class _Node:
        """Structure storing the underlying data and relevant links for
        use by the tree class's methods."""
        __slots__ = '_element', '_parent', '_children' # to make lighter in memory
        #   Will the _children thing work for an arbitrary number of children?

        # Is there some smarter data structure to use than a list-array for
        # children? Maybe a hash table since we're assuming nonordered
        # children?
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
            self._children = children if children is not None else []

    # ----------------------- nested Postiion class --------------------------

    # Public because we want the element() accessor method to be public, per
    #   the ADT. 

    class Position:
        """Abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor not meant to be invoked by external user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same
            location.

            Args:
                other (object): Any type of object

            Returns:
                (bool): True if other is a Postition representing the same
                    location, else False.
            """
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Validate position and return the associated node if valid.

        Returns:
            (_Node): the _Node object at position, if position validly exists
                in the tree.
        """
        if not isinstance(p, self.Position):
            raise TypeError("'p' arg must be proper Position type")
        if p._container is not self:
            raise ValueError("'p' arg does not belong to this container")
        if p._node._parent is p._node: # convention for deprecated nodes
            raise ValueError("'p' is no longer valid")
        return p._node

    def _make_position(self, node):
        """
        Return Position instance for given node (or None if no node).

        Args:
            node (_Node): _Node object

        Returns:
            (Position): New Position instance with node as the value of its
                _node instance variable.
        """
        return self.Position(self, node) if node is not None else None

    # ----------------------- general tree constructor ----------------------
    def __init__(self):
        """Create an initially empty general tree."""
        self._root = None
        self._size = 0

    # ------------------------- nonpublic updaters ---------------------------

    def _add_root(self, e):
        """
        Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty.

        Args:
            e (object): Element to be stored at root.

        Returns:
            (Position): New Position object represnting tree's root.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_child(self, p: Position, e):
        """Create a new child for Position p, storing element e. Raise
        ValueError if Position p is invalid. 
        
        Returns:
            (Position): Position of the new Node.
        """
        # append the new Position obj to p._Node._children list
        node = self._validate(p)
        self._size += 1
        new_node = self._Node(element=e, parent=node) # new child _Node object
        node._children.append(new_node) # add it to parent node's children list
        return self._make_position(new_node) # make a position object

    def _replace(self, p, e):
        raise NotImplementedError

    def _attach(self, p: Position, other_tree) -> None:
        """Attach tree other_tree as a child-subtree of Position p."""

        # Unlike in LBT, we don't care about whether p was external, right?
        #   Because no limitation on number of children.
        raise NotImplementedError
    
    def _delete(self, p):
        """
        Delete the node at Position p, and replace it with its child, if
        it has exactly one child.

        Return the element that had been stored at Position p. RaiseValueError
        if Position p is invalid or has more than 1 child.
        """
        child = None
        node = self._validate(p)
        if self.num_children(p) > 1: raise ValueError("p has multiple children")
        if self.num_children(p) == 1:
            child = node._children[0] # better for time or space to list.pop()?
        if child is not None:
            child._parent = node._parent # child's grandparent becomes parent
        if node is self._root:
            self._root = child # child becomes root
        else:
            parent = node._parent
            # todo not sure the adaptation from the LBT code is correct here,
            #   wrt skipping the if node is parent._left stuff
            # Might be fine though. This child's child would be "pulled up"
            #   with it by the promotion, without any further action, right?
        self._size -= 1
        node._parent = node # convention for deprecated node (make it its own parent)
        return node._element

    

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
        # Hasty implementation bc needed to test delete, may not be smartest
        #   But builtin len(list) should run in O(1) no different from
        #   storing an instance variable num_children for each node.
        return len(position._node._children)

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
