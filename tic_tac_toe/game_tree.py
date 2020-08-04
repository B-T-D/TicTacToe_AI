from tic_tac_toe.general_tree import GeneralTree, LinkedQueue
from tic_tac_toe.board import TicTacToeBoard

import copy

class GameTree(GeneralTree):
    """Tree of possible tic tac toe game states."""

    class _Node(GeneralTree._Node): # override GeneralTree's _Node class

        def __init__(self, element, parent=None, children=None):
            super().__init__(element, parent, children)

        # TODO should score initialize to None? See if 0 causes minimax implementation probs

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

    def _swap_player(self, player):
        return 2 if player == 1 else 1

    def legal_moves(self, board, player):
        """
        Return a list of all legal moves available to player based on current
        state of board.

        Args:
            board (list): 3 x 3 array of representing a tic tac toe board in
                0 / 1 / 2 notation convention.
            player (int): 1 or 2 corresponding to which player's turn it is.
        
        Returns:
            (list): List of two-element tuples representing the (row, col)
                coordinates at which player could legally place a mark on the
                next turn.
        """
        # caller will call this with
        #   mygametree.legal_moves(myboard.board(), myboard.player()
        raise NotImplementedError

    def check_tie(self, board, player):
        """
        Return True if no possible legal moves on board allow either player
        to win, else False."""
        raise NotImplementedError

    def optimal_move(self, board, player):
        """
        Return the optimal next move for player based on state of board, as a
        two-element (row, column) tuple."""
        raise NotImplementedError

    def build_essentially_different_moves():
        """Build subtree of all essentially different moves. All legal moves,
        excluding moves that could be made by rotations and reflections of an
        already known legal move."""
        raise NotImplementedError

    def _validate_board(self, board):
        """
        Validate that board is a 3x3 two-dimensional array with each element
        equal to one of 0, 1, or 2. Return board if valid, else raise an
        error to the caller.
        """
        raise NotImplementedError

    def _validate_element(self, e):
        """
        Validate that e is a valid element: a two-element tuple of
        (board: list, score: int).
        :param board:
        :return:
        """
        raise NotImplementedError

    def compute_score(self, position) -> int:
        """Return the value of the node at position to appropriate int value to the caller.
        
        If node is a leaf, assign 1 for player-win, 0 for draw, -1 for
        opponent win. If node not leaf, take the min or max of the value returned
        by recursively calling compute_value() on each of position's children.
        """
        # Recursive implementation here is a nonfunctional mess, but this should be the conceptual
        #   essence of the minimax algorithm. 
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
                print("-------REturned from first if condition")
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
        board_copy = TicTacToeBoard(board=grid_copy,
                                    player=position.element().player())
                                    # player shouldn't be flipped yet because it flips when .mark() is called
        return self._add_child(position, board_copy)

