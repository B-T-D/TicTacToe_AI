from tic_tac_toe.general_tree import GeneralTree, LinkedQueue
from tic_tac_toe.board import TicTacToeBoard

import copy
import random

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


    def optimal_move(self, board):
        """
        Return the optimal next move for player based on state of board, as a
        two-element (row, column) tuple.

        Args:
            board (TicTacToeBoard): TicTacToeBoard object.

        Returns:
            (tuple): (row, column) coordinates of optimal move for board's
                active player.
        """
        # todo wrapper for the internal _subtree_optimal_score. Encapsulate everything else
        #   so when the tree builder algo and tree-storage is improved, calls to this method
        #   are unaffected.

        # todo it may have no mechanism for valuing faster wins more than
        #   slower wins--appeared to pass on a chance to win in one move in a
        #   game where its eventual win was guaranteed either way.

        # Bypass the ultra-slow full-tree build until algorithm fixed.
        #   If it's a blank board, randomly return one of the corners in
        #   O(1) time.
        if board.board() == [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]:
            return self._random_corner()
        # Todo Return center square in O(1) time if opponent moved first into a corner.
        #   Don't want it to auto-pick a corner any time any corner is free.

        if self._first_move_in_corner(board.board()):
            return (1, 1)

        # Make board the root of the tree:
        self._add_root(board)
        # Internal methods can handle it from there:
        return self._subtree_optimal_move(self.root())

    def _random_corner(self):
        """Return tuple corresponding to coordinates for randomly chosen corner
        of the board."""
        r = random.random()
        if r < (1/4):
            return (0,0)
        elif r < (1/2):
            return (0,2)
        elif r < (3/4):
            return (2, 0)
        else:
            return (2, 2)

    def _first_move_in_corner(self, grid):
        """Inspect each corner of the grid to determine if opponent made first
        move into a corner. Shortcut method to return early when AI is moving
        second.

        Args:
            grid (list): 3 x 3 array representing tic tac toe grid.

        Returns:
            (bool): True if opponent played in a corner, else False
        """
        # todo collapse all into max one-linerism
        if grid[0][0] != 0 or grid[0][2] != 0:
            # inspect rows 1 and 2 first, since a non zero there would rule out
            #   both cases:
            for row in range(1, 3): # inspect full rows 1 and 2
                if sum(grid[row]) != 0: return False
            if grid[0][0] != 0:
                for i in range(1,3): # inspect remainder of row 0
                    if grid[0][i] != 0: return False
            elif grid[0][2] != 0:
                for i in range(2): # inspect the two preceeding row 0 sqares
                    if grid[0][i] != 0: return False
        elif grid[2][0] != 0 or grid[2][2] != 0:
            # first try to rule out both via a different row:
            for row in range(2):
                if sum(grid[row]) != 0: return False
            if grid[2][0] != 0:
                for i in range(1, 3):
                    if grid[2][i] != 0: return False
            elif grid[2][2] != 0:
                for i in range(2):
                    if grid[2][i] != 0: return False
        return True


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
        Add child of position and apply move to it. Does not set score for
        the new child.

        Args:
            position(Position): Position in this tree with a TicTacToeBoard
                object as its element.
            move (tuple): (row, coordinate) tuple.

        Returns:
                (Position): Position object for the new child node.

        """
        child = self._add_unmarked_child(position) # todo prob will be able to collapse later
        child.element().mark(move[0], move[1])
        child._node._move = move
        # todo NB: Can't compute the score here because you don't know the value
        #   of _player for the relevant root. Score depends on the top-level
        #   player, i.e. who's calling minimax. You can only know positive vs.
        #   negative relatively via tree.depth(child) after you know who the
        #   player is at depth=0.


        return child


    def _possible_moves(self, position) -> list:
        """
        Return a list of tuples representing the possible moves from
        position's boardstate.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                object as its element.

            moves_queue (LinkedQueue): LinkedQueue to put possible moves in.

        Returns:
            (LinkedQueue): LinkedQueue of (row, column) tuples
        """
        moves = []
        grid = position.element().board()
        for row in range(len(grid)): # iterate over all squares in the grid:
            for col in range(len(grid[row])):
                if grid[row][col] == 0:
                    moves.append((row, col))
        return moves

    def _enqueue_moves(self, moves_list, moves_queue):
        """Helper method to add each move in a moves_list to a moves_queue."""
        for move in moves_list:
            moves_queue.enqueue(move)

# Todo: Make a separate movesqueue object with method MovesQueue._possible_moves(Position) ?

    def _build_children(self, position, children_queue):
        """
        Build children of position, one child for each of position's possible
        moves.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                object as its element.

        Returns:
            None
        """
        if position.element().winner() is not None: # Don't waste time trying to add children to a gameover board.
            return
        moves_queue = LinkedQueue()
        # a move leaves the moves queue, becomes a child, and enters the child queue
        self._enqueue_moves(self._possible_moves(position), moves_queue)
        while not moves_queue.is_empty():
            move = moves_queue.dequeue()
            new_child = self._add_marked_child(position, move)
            children_queue.enqueue(new_child)
             # add the new child's possible moves to the queue.


    def _build_tree(self, position): # todo collapse into or only call from __init__
        """
        Build subtree of all possible boardstates reachable from position's
        boardstate.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                as its element. Defaults to root.
        """
        children_queue = LinkedQueue()
        self._build_children(position, children_queue) # this will enqueue some children
        while not children_queue.is_empty():
            child = children_queue.dequeue()
            self._build_children(child, children_queue)

    def compute_score(self, position) -> int:
        """Return the score of the node at position to appropriate int value to the caller.

        If node is a leaf, assign 1 for player-win, 0 for draw, -1 for
        opponent win. If node not leaf, take the min or max of the value returned
        by recursively calling compute_value() on each of position's children.
        """
        node = self._validate(position)
        if self.is_leaf(position):  # base case
            winner = position.element().winner()
            if winner == position.element().player():  # what .player() returns at this point in execution
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
                # print("-------Returned from first if condition")
                return 1
            elif winner == position.element().opponent():  # "opponent" here means the original minimax caller
                # print("-------------returned from elif")
                return -1
            else:  # value should be none
                # print("-----------Returned from else----------------")
                return 0  # if it's a leaf and board.winner() returns None, that should indicate
                #   a tie (rather than an incomplete game).
        # Need to call depth() here I think, because need to alternate min and maxing with each
        #   layer of children you recurse through.
        elif self.depth(position) % 2 == 0:  # max at even numbered layers
            child_values = [self.compute_score(i) for i in
                            self.children(position)]
            return max(
                child_values)  # collapse to one liner max(listcomp) if this is correct
            # compare with recursive delete for how to iterate children while recursing
        elif self.depth(position) % 2 == 1:  # min at odd numbered layers
            child_values = [self.compute_score(i) for i in
                            self.children(position)]
            return (min(child_values))

    def _score_leaf(self, position):
        if not self.is_leaf(position):
            raise ValueError("Position must be a gameover leaf.")
        player = self.root().element().player() # want the top-level player, not necessarily this node's player
        opponent = self.root().element().opponent() # todo recompress for conciseness
        winner = position.element().winner() # want this position's winner though, not root's (root has no winner by definition)

        if winner == player:
            score = 1
            position._node._score = score
            return score
        elif winner == opponent:
            score = -1
            position._node._score = score
            return score
        elif winner == 3:
            score = 0
            position._node._score = score
            return score


    def _score_subtree(self, position):
        """
        Update the score attribute for the node at each Position in the
        subtree rooted at Position.

        Args:
            position (Position): Position in this tree with TicTacToeBoard
                as its element, with full set of subtrees all eventually
                terminating in a gameover-leaf.
        Returns:
            None
        """
        # print("---------------------------------")
        # print(f"_score_tree called on \n{position.element()}")
        if self.is_leaf(position):
            # print(f"scoring gameover leaf")
            return self._score_leaf(position)
        else: # following 5 lines are just a long-winded "elif all children are scored"
            child_scores = [] # todo does it make sense to opportunistically build the list here, to reduce number of passes through children? or wasteful?
            children_scored = True # todo how is there not a more concise listcomp way to check if all children are scored?
            for child in self.children(position): # todo store it as an instance variable of each Position?
                if child.score() is None:
                    children_scored = False
                else:
                    child_scores.append(child.score())
            if children_scored == True:
                child_scores = [c.score() for c in self.children(position)]
                # print(f"child_scores = {child_scores}")
                if self.depth(position) % 2 == 0:
                    # print(f"taking max of child scores")
                    score = max(child_scores)
                    position._node._score = score
                    return score
                elif self.depth(
                        position) % 2 == 1:  # todo compress once it works, e.g. shouldn't need an elif or even an else here if logic is correct
                    # print(f"taking min of child scores")
                    score = min(child_scores)
                    position._node._score = score
                    return score
        # Recursive case -- internal node with unscored children
        # print(f"position was not leaf and did not have scored-children leaves")
        for child in self.children(position):
            self._score_subtree(child)
        return self._score_subtree(position) # re-call the function on original position after all children scores


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
        self._build_tree(position) # Build the tree...
        self._score_subtree(position) # ...and score it.
        max_score = -10 # Must be < -1
        best_move = None
        for child in self.children(position):
            # print(f"child is \n{child.element()}"
            #       f"\n\tscore = {child.score()}"
            #       f"\n\tmove to child  = {child.move()}")
            if child.score() > max_score:
                max_score = child.score()
                best_move = child._node._move
        return best_move



