from tic_tac_toe.general_tree import GeneralTree
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
            player (int): 1 if X will move first, 2 if O.

        Returns:
            None
        """
        # todo probably won't be needed once things more sorted out

        self._build_layer(self.root(), player)
        prev_children = [c for c in self.children(self.root())]
        player = self._swap_player(player)
        for child in self.children(self.root()):
            self._build_layer(child, player)
        player = self._swap_player(player)
        for c in prev_children:
            print(f"root-child c has {self.num_children(c)} children")
            print(f"root-child c has element board {c.element()[0]}")
            self._build_layer(c, player)


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

    def compute_value(self, position):
        """Return the value of the node at position to appropriate int value to the caller.
        
        If node is a leaf, assign 1 for player-win, 0 for draw, -1 for
        opponent win. If node not leaf, take the min or max of the value returned
        by recursively calling compute_value() on each of position's children.
        """
        # Recursive implementation here is a nonfunctional mess, but this should be the conceptual
        #   essence of the minimax algorithm. 
        node = self._validate
        if node.is_leaf(): # base case
            winner = node._element._board.winner()
            if winner == player:
                return 1
            elif winner == opponent:
                return -1
            else: # value should be none
                return 0 # if it's a leaf and board.winner() returns None, that should indicate
                        #   a tie (rather than an incomplete game).
        # Need to call depth() here I think, because need to alternate min and maxing with each
        #   layer of children you recurse through.
        elif depth % 2 == 0: # max at even numbered layers
            child_values = [compute_value(i) for i in position.children()]
            return max(child_values) # collapse to one liner max(listcomp) if this is correct
                 # compare with recursive delete for how to iterate children while recursing
        elif depth % 2 == 1: # min at odd numbered layers
            return(min(compute_value(children)))

def test():
    print("hello world from game_tree")


if __name__ == '__main__':
    test()
