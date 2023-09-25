from space import *
    
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
            state_dict[tuple(line_hor)] = 0
            state_dict[tuple(line_ver)] = 0
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
        
        for line in self.line_map[loc[0]][loc[1]]:
            for attribute in range(4):
                self.quarto_state[line][attribute][piece.attribute_list[attribute]]+=1
                    
        
                
                

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