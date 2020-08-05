from tic_tac_toe.general_tree import GeneralTree, LinkedQueue
from tic_tac_toe.board import TicTacToeBoard

import copy

class GameTree(GeneralTree):
    """Tree of possible tic tac toe game states."""

    class _Node(GeneralTree._Node): # override GeneralTree's _Node class

        def __init__(self, element, parent=None, children=None,
                     move=None, score=None):
            """

            :param element (TicTacToeBoard): a TicTacToeBoard object
            :param parent:
            :param children:
            :param move: The move that produced this node's boardstate, else
                None for a blank board.
            :param score: This node's score as computed by the minimax method,
                else None.
            """
            # todo: What about __slots__? That won't have move and score.
            super().__init__(element, parent, children)
            self._move = move
            self._score = score

        # TODO should score initialize to None? See if 0 causes minimax implementation probs

    class Position(GeneralTree.Position):
        """Extensions to inherited Position nested-class to support accessor
        methods for Node._move and Node._score."""

        def __init__(self, container, node): # No changes. Move and score are
                                            #   encapsulated within object that's
                                            #   passed as node arg.
            super().__init__(container, node)

        def move(self):
            """Return the move that resulted in the creation of the boardstate
            stored at this position. For example, if the Position stores
            a boardstate representing X moving first by marking (0,1),
            Position.move() will return (0, 1).

            Returns:
                (tuple): Two-element (row, column) tuple representing coordinates
                    of a square on the TicTacToeBoard.
            """
            return self._node._move

        def score(self):
            """Return the minimax score of the boardstate stored at this
            Position.

            Returns:
                (int): -1, 0, or 1.
            """
            return self._node._score

    # Haven't actually needed to override GeneralTree's __init__, yet.

    def _add_root(self, element, move=None, score=None):
        """Override of inherited method to support adding move and score in addition
        to element."""
        # todo seemed most expedient not to try to integrate a super() call to
        #   the inherited _add_root, because it tangles into the GeneralTree's
        #   make_position and calls GeneralTree's Position constructor instead.
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(element, move, score)
        return self._make_position(self._root)


    def build_dumb_tree(self, position, player):
        """Build a redundant tree of all possible moves in a game, ignoring
        that some elements won't represent essentially distinct positions
        (first move X in one corner isn't essentially distinct from a different
        corner, etc.).

        Args:
            postion (Position): Position that will be root of the subtree
            player (int): 1 if X will move first, 2 if O.

        Returns:
            None
        """
        # todo probably won't be needed once things more sorted out
        qpos = LinkedQueue() # shorthand for "queued positions". The queue will store new positions
        # in the order they were added.
        start_player = player # Store for expedient player-identification when deeper in tree
        qpos.enqueue(position)

        while not qpos.is_empty():
            parent = qpos.dequeue()
            board = parent.element()[0]

            for i in range(3): # This would be O(n^2) for n = gridsquares in the board.
                                # For now we can assume always a 3 x 3 board, not
                                #   an arbitrarily large one.
                            # If you're iterating over a square (the board),
                                # you'll have a 'square' looking loop nesting;
                                #   a square is rows * columns.
                for j in range(3):
                    if board[i][j] == 0: # if blank square available for marking
                        child_board = copy.deepcopy(board)
                        if self.depth(parent) % 2 == 1: # odd-numbered layer in this subtree
                            player = self._swap_player(start_player) # ...means it's start_player's opponent's turn.
                        else:
                            player = start_player
                        child_board[i][j] = player # mark the board
                        child_element = (child_board, 0) # implementation housekeeping for ._element tuple
                        new_pos = self._add_child(parent, child_element)
                        qpos.enqueue(new_pos)



        # self._build_layer(self.root(), player)
        # prev_children = [c for c in self.children(self.root())]
        # player = self._swap_player(player)
        # for child in self.children(self.root()):
        #     self._build_layer(child, player)
        # player = self._swap_player(player)
        # for c in prev_children:
        #     print(f"root-child c has {self.num_children(c)} children")
        #     print(f"root-child c has element board {c.element()[0]}")
        #     self._build_layer(c, player)


        # self._build_layer(position, player)
        # player = self._swap_player(player)
        # print(self.num_children(position))
        # for child in self.children(position):
        #     self._build_layer(child, player)

        # for position in self.tree.positions()
        #  todo breadth first

        # self._build_layer(position, player)
        #
        # if not self.is_leaf(position):
        #     player = self._swap_player(player)
        #     for child in self.children(position):
        #         self.build_dumb_tree(child, player)



    def _build_layer(self, position, player):
        """Build a layer of children of position by adding one child for each
        remaining blank square, each child's element's board marking a different
        square.

        Returns:
            (bool): True if any children were added, else False
        """
        children_added = False
        board = position.element()[0]
        print(f"_build_layer thinks board is {board}")
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    child_board = copy.deepcopy(board) # todo shallow vs. deep better here?
                    child_board[i][j] = player # mark with 1 or 2
                    child_element = (child_board, 0)
                    print(f"adding childboard {child_board}")
                    self._add_child(position, child_element)
                    children_added = True
        return children_added

    def optimal_move(self, board, player):
        """
        Return the optimal next move for player based on state of board, as a
        two-element (row, column) tuple."""
        raise NotImplementedError

    def compute_score(self, position) -> int:
        """Return the value of the node at position to appropriate int value to the caller.
        
        If node is a leaf, assign 1 for player-win, 0 for draw, -1 for
        opponent win. If node not leaf, take the min or max of the value returned
        by recursively calling compute_value() on each of position's children.
        """
        node = self._validate(position)
        if self.is_leaf(position): # base case
            winner = position.element().winner()
            if winner == position.element().player(): # what .player() returns at this point in execution
                                                        # is actually the opponent of who just moved.
                                                        # player() tells the caller "after the most recent .mark()
                                                        # call placed a mark, it became this person's turn:".
                                                        # If X places a mark with a .mark() call, and wins, the
                                                        # ._player attribute of the TicTacToeBoard that returns X
                                                        # for .winner() is O, not X.

                                                        # Here, position.element().player() isn't necessarily
                                                        # the player running the minimax algorithm. It's the
                                                        # player who would get to move next if this node
                                                        # weren't a gameover leaf.

                                                        # ".player()" might be better named "mover".
                print("-------Returned from first if condition")
                return 1
            elif winner == position.element().opponent(): # "opponent" here means the original minimax caller
                print("-------------returned from elif")
                return -1
            else: # value should be none
                print("-----------Returned from else----------------")
                return 0 # if it's a leaf and board.winner() returns None, that should indicate
                        #   a tie (rather than an incomplete game).
        # Need to call depth() here I think, because need to alternate min and maxing with each
        #   layer of children you recurse through.
        elif self.depth(position) % 2 == 0: # max at even numbered layers
            child_values = [self.compute_score(i) for i in self.children(position)]
            return max(child_values) # collapse to one liner max(listcomp) if this is correct
                 # compare with recursive delete for how to iterate children while recursing
        elif self.depth(position) % 2 == 1: # min at odd numbered layers
            child_values = [self.compute_score(i) for i in self.children(position)]
            return(min(child_values))

    def _add_unmarked_child(self, position):
        """
        Add a child of position, which child's element being a not-yet-marked
        copy of the board stored at parent position.

        Args:
            position (Position): Position object with a TicTacToeBoard object
                as its element.

        Returns:
            (Position): Position object for the new child node.
        """
        # Make a deepcopy of the underlying 3x3 grid:
        grid_copy = copy.deepcopy(position.element().board())
        # Use that copy to make a new TicTacToeBoard object that starts with
        #   same values in its grid, and with its player set to parent
        #   position's player:
        board_copy = TicTacToeBoard(grid=grid_copy,
                                    player=position.element().player())
                                    # player shouldn't be flipped yet because it flips when .mark() is called
        return self._add_child(position, board_copy)

    def _add_marked_child(self, position, move: tuple):
        """
        Add child of position and apply move to it.

        Args:
            position(Position): Position in this tree with a TicTacToeBoard
                object as its element.
            move (tuple): (row, coordinate) tuple.

        Returns:
                (Position): Position object for the new child node.

        """
        raise NotImplementedError

    def _possible_moves(self, position):
        """
        Return a list of tuples representing the possible moves from
        position's boardstate.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                object as its element.

        Returns:
            (list): List of (row, column) tuples
        """
        raise NotImplementedError

    def _build_children(self, position):
        """
        Build children of position, one child for each of position's possible
        moves.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                object as its element.

        Returns:
            None
        """
        raise NotImplementedError

    def _build_tree(self, position): # todo collapse into or only call from __init__
        """
        Build subtree of all possible boardstates reachable from position's
        boardstate.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                as its element. Defaults to root.
        """

        raise NotImplementedError

    def _score_subtree(self, position):
        """
        Update the score attribute for the node at each Position in the
        subtree rooted at Position.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                as its element. Defaults to root.
        Returns:
            None
        """
        # todo tests should confirm this (and any other visit-action) methods
        #   are breadth first
        raise NotImplementedError

    def _subtree_optimal_move(self, position):
        """
        Return the optimal move coordinates for position's boardstate. Meant
            to be called with self.root() as the position argument.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                as its element. Defaults to root.

        Returns:
              (tuple): (row, column) tuple representing the optimal move.
        """
        raise NotImplementedError



