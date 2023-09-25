from gamestate import *

    
        
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
    def get_available_spaces(self):
        available_spaces = []
        for row in range(4):
            for col in range(4):
                if self.game.at(row, col).is_free():
                    available_spaces.append((row,col))
        return available_spaces

    def pick(self):
        available_pieces = [idx for (idx,i) in enumerate(self.game.pieces) if i is not None]
        piece_index = random.choice(available_pieces)
        return self.game.pick(piece_index)

    def play(self,piece,last_play):
        available_spaces = self.get_available_spaces()
        return random.choice(available_spaces)

class DefensiveAgent(RandomAgent):
    def will_win(self, space, piece):
        space_lines = self.game.board.line_map[space[0]][space[1]]
        for line in space_lines:
            for attribute in range(4):
                if self.game.board.quarto_state[line][attribute][piece.attribute_list[attribute]]+1 == 4:
                    return True
        return False
        
    def play(self, piece, last_play):
        available_spaces = []
        for row in range(4):
            for col in range(4):
                if self.game.at(row, col).is_free():
                    available_spaces.append((row,col))
        

        for space in available_spaces:
            if self.will_win(space, piece):
                return space
        return random.choice(available_spaces)

class OffensiveAgent(DefensiveAgent):

    def is_ok(self,piece,available_spaces,available_pieces):
       
        for space in available_spaces:
            space_lines = self.game.board.line_map[space[0]][space[1]]
            for line in space_lines:
                for attribute in range(4):
                    if self.game.board.quarto_state[line][attribute][Piece(piece).attribute_list[attribute]]+1 == 4:
                        return False
        return True
                
    def pick(self):
        available_pieces = [idx for (idx,i) in enumerate(self.game.pieces) if i is not None]
        available_spaces = self.get_available_spaces()
        
        ok_pieces = [piece for piece in available_pieces if self.is_ok(piece,available_spaces, available_pieces)]
        print(f"ok pieces: {ok_pieces}")
        if len(ok_pieces)==0:
            return self.game.pick(random.choice(available_pieces))
        return self.game.pick(random.choice(ok_pieces))
        
        

class SabotageAgent(OffensiveAgent):

    def can_sabotage(self,piece,line):
        sabotagability = False
        for attribute in range(4):
            if self.game.board.quarto_state[line][attribute][piece.attribute_list[attribute]]==0 and self.game.board.quarto_state[line][attribute][int(not piece.attribute_list[attribute])]>0:
                sabotagability = True
            elif self.game.board.quarto_state[line][attribute][piece.attribute_list[attribute]]>0 and self.game.board.quarto_state[line][attribute][int(not piece.attribute_list[attribute])]==0:
                return False
        return sabotagability
        
    def play(self,piece, last_play):
        available_spaces = self.get_available_spaces()
        for space in available_spaces:
            if self.will_win(space, piece):
                return space
        sabotagabilities = {}

        for space in available_spaces:
            sabotagability = 0
            for line in self.game.board.line_map[space[0]][space[1]]:
                if self.can_sabotage(piece, line):
                    sabotagability+=1
            sabotagabilities[space] = sabotagability
        best_sabotager = max(zip(sabotagabilities.values(), sabotagabilities.keys()))[1] 
        if sabotagabilities[best_sabotager]>0:
            return best_sabotager
        return random.choice(available_spaces)
        
        