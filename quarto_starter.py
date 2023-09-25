import random
#!/usr/bin/env python3

from itertools import cycle

"""
  Welcome to your Final Project for AMP, Quarto.

  This project is the _most_ open ended project so far.
  Your task is to program an automatic quarto player. As with the
  Wordle Project, please think carefully about the experimental design
  to validate that your successive players are indeed improvements.

  === 0. WARMUP TASK === 

  However, before you start exploring, you should get familiar with the
  starter code.

  As a warmup task, implement the check_quarto method in the Board class,
  which checks whether there is a quarto on the board.

  === 1. BASELINE RANDOMNESS ===

  As with wordle, build a random player as a baseline.
  - For pick moves, pick a random Piece.
  - For play moves, pick a random location on the board.
  
  Research Question:
  - Who wins more often? Player 1 or Player 2? Why?

  === 2. OFFENSIVE GAME AGENT ===

  Build a game agent that plays a quarto if it can!
  
  Specifically, in play(self, piece), if playing piece in some location loc
  makes it the fourth piece in a quarto, play it there.
  If you can't make a quarto with the provided piece, randomly select from
  the list of locations that do _not_ create a quarto on the board.

  Please inherit from the RandomAgent so that your _pick_ algorithm
  is still random.

  Empirical Question:
  - How does this algorithm compare to the Random Agent? Does it _always_ win?
  
  === 3. A DEFENSIVE GAME AGENT ===

  Build a game agent that takes defensive moves in the pick method.

  Specifically in pick(self), do not select a piece that enables your opponent to win!
  That is, the piece you pass them should not form a quarto. Pick a random piece from
  the remaining pieces. 

  Research Question:
  - How does this algorithm compare to the Offensive Agent? To the Random Agent?
    
  === 4. GENERALIZING -- BREADTH-FIRST SEARCH? ===

  Generalize these observations into a breadth first search!
  Create a search tree where the children of each node are the 
  next possible game states. Notice that there are two kinds of 
  steps you can take (Pick, Play).

  It is not tractable to run a breadth first search over 
  the space of all approximately 16!^2 games.
  - How many games are there?
  - Try running some python code to count up to that number.
    How long does it take? Is this feasible?

  How deep can you go in your search? That is, try adding a max-depth
  parameter (like max_rungs from word ladders) and testing how many moves 
  ahead you can you look before your BFS starts to feel sluggish? Can you use
  this as a subroutine?

  Once you've constructed a BFS, you can't be sure, in the common case,
  what the outcome of the game will be. How do you "score" the intermediate
  game states?
  
*************************************************

Now is the time for your creativity to shine. Your task is "simply"
to build better and better game playing agents!

Here are some things I've thought about, but you are welcome to do whatever
comes to mind! Do make sure to justify your approaches analytically and 
experimentally. You will all give presentations on the last day of class (8/3).
- Hybrid Approaches:
   * In chess, the opening, midgame, and late game have different
     strategies. Are there equivalent strategies here?
   * Can you combine some of the above solvers? Make your own?
   * Go wild!
- Implementing human strategies. 
   * How do you play the game? 
   * Can you codify your human strategies into automatic agents? 
- Optimization
   * The goal here is to increase the tractable depth of the BFS Agent.
   * Can you optimize the Breadth-First Search? Here are some ideas:
      + Loops vs recursion, exploit confluent board states,
        pre-computation, incremental computation, 
        symmetry reduction, parallelism

"""

class colors:
    ENDC = '\u001b[0m'
    CYAN = '\u001b[36m'
    GREEN = '\u001b[36m'
    BOLD = '\u001b[37;1m'
    RVRS = '\u001b[7m'
    UNDR = '\u001b[4m'
    UNUNDER = '\u001b[24m'

class Piece():

    def __init__(self, n):
        """
        A piece has 4 attributes:
          its color, its size, whether it has a hole, and its shape
        Since there are 2^4 distinct pieces, we can initialize and uniquely
        identify a piece with a number between 0 and 15.

        This constructor creates a piece from such an identifying integer n

        CAUTION :: These fields should be treated as READ ONLY.
        Outside of this method, do not assign to them. Rather than modifying a piece,
        create a new one.
        """
        self.color = n % 2 == 1
        self.size = (n>>1) % 2 == 1
        self.holey = (n>>2) % 2 == 1
        self.shape = (n>>3) % 2 == 1
        self.ident = n
        self.attribute_list = (int(self.color), int(self.size), int(self.holey), int(self.shape))

    def get_attribute_list(self):
        return self.attribute_list

    def __str__(self):
        """
        The __str__ method allows you to call str(p) for a piece p

        We represent each attribute using stylized ASCII.
        * color - the symbol for a piece is either CYAN or your terminal default.
                  In Default VSCode this is white.
        * size  - A tall piece will be underlined. A short piece will not be.
        * holey - A piece with a hole is indicated via an asterix *
        * shape - A "round" piece is indicated by ( ) and a square piece by [ ]
        """
        return "{strtc}{height}{left}{hole}{right}{unundr}{endc}".format(
            strtc  = colors.CYAN if self.color else "",
            endc   = colors.ENDC if self.color else "",
            left   = "(" if self.shape else "[",
            right  = ")" if self.shape else "]",
            hole   = "*" if self.holey else " ",
            height = colors.UNDR if self.size else "",
            unundr = colors.UNUNDER if self.size else "",
        )
    
    def __eq__(self, other):
        return self.ident == other.ident

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

class Board():
    def __init__(self):
        """
        A board is a 4x4 board, represented as a two dimensional matrix
        aka a list of lists.
        """
        self.board = [
            [Space() for _ in range(4)]
            for _ in range(4)
        ]

        
        #initalizes what blocks maps to what lines
        line_map = [[[] for i in range (4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                line_map[i][j].append(i)
                line_map[i][j].append(j+4)

        for i in range(4):
            line_map[i][i].append(8)
            line_map[i][3-i].append(9)

        self.line_map = line_map
        
        state_dict = {}
        line_fdiag = []
        line_bdiag = []  
        for i in range(4):
            line_hor = []
            line_ver = []
            line_fdiag.append((i,i))
            line_fdiag.append((i,3-j))
            for j in range(4):
                line_hor.append((i,j))
                line_ver.append((j,i))
            line_hor = tuple(line_hor)
            line_ver = tuple(line_ver)
            state_dict[line_hor] = 0
            state_dict[line_ver] = 0
        state_dict[tuple(line_fdiag)] = 0
        state_dict[tuple(line_bdiag)] = 0

        self.state_dict= state_dict
                


        #initializes states
        self.quarto_state = [[[0,0] for i in range(4)] for i in range(10)]
        # self.last_played = None

    
    '''
    def update_last_played(self, row, column, piece):
        self.last_played = [Piece(piece), row, column]
        last_played_attributes =  self.last_played[0].get_attribute_list()
        for (attribute, type) in last_played_attributes:
            for line in self.line_map[row][column]:
                self.quarto_state[line][attribute][type]+=1
    '''
    def update_state(self, piece,loc):
        for line in range(10):
            for attribute in range(4):
                self.game.board.quarto_state[attribute][piece.attribute_list[attribute]]+=1

    def __str__(self):
        out = "     "
        for i in range(4):
            out += str(i) + (" " * 5)
        out += "\n"
        for (i,row) in enumerate(self.board):
            out += "  " + ("-" * (4 * 6 + 1))
            out += "\n"
            out += chr(ord("A") + i) + " "
            for col in row:
                out += "| " + str(col) + " "
            out += "|\n"
        out += "  " + ( "-" * (4 * 6 + 1))
        return out

    def at(self, row, col):
        """
        Gets the Space at the provided row and column.

        If row and column are out of bounds, this method returns False.
        """
        if row >= 4 or col >= 4 or row < 0 or col < 0:
            return False
        else:
            return self.board[row][col]

    def has_quarto(self):
        """
        returns True if 4 in a row, column or diagonal of the same type occur on the board.
        """
        for i in range(10):
            for j in range(4):
                for k in range(2):
                    if self.quarto_state[i][j][k]==4:
                        return True

        return False

    def game_over(self):
        """
        returns true if all pieces have been played
        """
        return all([all([space.contents is not None for space in row])
                    for row in self.board])

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

class Player ():
    def __init__(self, ident, game):
        """
        Create a Human player with identifier indent
        for the game state game
        """
        self.game = game
        self.ident = str(ident)

    def __str__(self):
        return str(self.ident)

    def pick(self):
        """
        Solicit a piece from the user and update the game state
        """
        str_index = input("player " + str(self) + ", pick a piece: ")
        piece_index = int(str_index.strip())
        return self.game.pick(piece_index)

    def play(self, piece, last_play):
        """
        Ask the player to play the piece.
        Also inform them of their opponent's last_play.

        A human player ignore this last_play, but an automatic player
        may want to use it
        """
        location = input("player " + str(self) + ", pick a place for " + str(piece) + ": ")
        row = ord(location[0].lower()) - ord("a")
        col = int(location[1:])
        return (row,col)


class RandomAgent(Player):
    def pick(self):
        available_pieces = [idx for (idx,i) in enumerate(self.game.pieces)]
        piece_index = random.choice(available_pieces)
        return self.game.pick(piece_index)

    def play(self,piece,last_play):
        available_spaces = []
        for row in range(4):
            for col in range(4):
                if self.game.at(row, col).is_free():
                    available_spaces.append((row,col))
        
        return random.choice(available_spaces)

class DefensiveAgent(RandomAgent):
    def play(self, piece, last_play):
        available_spaces = []
        for row in range(4):
            for col in range(4):
                if self.game.at(row, col).is_free():
                    available_spaces.append((row,col))
        

        for space in available_spaces:
            space_lines = self.game.board.line_map[space[0]][space[1]]
            for line in space_lines:
                for attribute in range(4):
                    if self.game.board.quarto_state[attribute][piece.attribute_list[attribute]] +1 == 4:
                        return space
        return random.choice(available_spaces)

class OffensiveAgent(DefensiveAgent):
    def pick(self):
        available_pieces = [idx for (idx,i) in enumerate(self.game.pieces) if i != None]
        available_spaces = []
        for row in range(4):
            for col in range(4):
                if self.game.at(row, col).is_free():
                    available_spaces.append((row,col))
        

    




class GameDriver ():
    def __init__(self, player1, player2):
        """
        The GameDriver runs the game for both players.
        ARGS
          - player1 and player2 are constructors that take 2 arguments,
            an identifier and the game state.
        ATTRIBUTES
          - self.game is the GameState
          - self.players is a cyclic list of players constructed from
            player1 and player2
        """
        self.game = GameState()
        self.players = cycle([player1(1, self.game), player2(2, self.game)])

    def run(self):
        """
        The main game loop. Runs the game until its over.
        """
        player = next(self.players)
        loc = None
        while not self.game.board.has_quarto() and not self.game.board.game_over():
            self.game.print_game_state()
            piece = player.pick()
            player = next(self.players)
            played = None
            while not played:
                loc = player.play(piece, loc)

                played = self.game.at(*loc).play(piece)

                if played:
                    pass
                    
                


        print("Player", str(player), "won!")
        self.game.print_game_state()
        print("Congrats player {}!".format(player))
        return player.ident

if __name__ == "__main__":
    g = GameDriver(RandomAgent, OffensiveAgent)
    g.run()
