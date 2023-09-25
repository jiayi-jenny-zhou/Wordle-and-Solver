from piece import *

class Space():
    """
    A Space represents a position on the board. It can be filled or empty
    """

    def __init__(self, piece = None):
        """
        Create a board with an optional instantiated piece.
        """
        self.contents = piece

    def play(self, piece):
        """
        Place a piece in the current Space.
        Return True if the move succeeded
        Return False if it failed because there was already a piece there
        """
        if self.contents is None:
            self.contents = piece
            return True
        else:
            return False

    def is_free(self):
        """
        Returns true if there is no piece in the current space
        """
        return self.contents is None

    def __str__(self):
        if self.contents is None:
            return "   "
        else:
            return str(self.contents)
