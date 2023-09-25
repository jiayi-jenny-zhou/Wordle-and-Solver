from board import *
class GameState():
    def __init__(self):
        """
        Create a GameState. It's attributes are 
        - self.board, the board in the game
        - self.piece, the pieces that can still be played
                      satisfying the invariant that when the
                      ith piece is played, self.piece[i] becomes
                      None
        """
        self.board = Board()
        # construct the 16 pieces
        self.pieces = [Piece(i) for i in range(4 ** 2)] 

    def gamestate_to_data(self):
        lines = []
        for col in range(4):
            for row in range(4):
                pass
    def print_game_state(self):
        stringify_piece = \
            lambda piece: \
            "     " if piece is None \
            else " {} ".format(str(piece))
        piece_str_list = ["{2}{0}: {1}".format(str(i) + (" " if i < 10 else ""),
                                             stringify_piece(piece),
                                             "\n  " if i % 4 == 0 else "")
                          for (i, piece) in enumerate(self.pieces) ]

        pieces_str = "Pieces:" + "  ".join(piece_str_list)

        print(pieces_str)
        print("**")
        print()
        print(self.board)
        print()

    def pick(self, idx):
        """
        Picks piece at index idx, setting self.pieces[idx] to None
        """
        if idx >= 4 ** 2: return None
        piece = self.pieces[idx]
        self.pieces[idx] = None
        return piece

    def at(self, row, col):
        """
        Return the board space at (row,col)
        """
        return self.board.at(row,col)