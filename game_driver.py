from player import *
        
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
                    self.game.board.update_state(piece, loc)
            if self.game.board.game_over() and not self.game.board.has_quarto():
                return "tie"
        


        print("Player", str(player), "won!")
        self.game.print_game_state()
        print("Congrats player {}!".format(player))
        return player.ident

def agent_tester(trials, agent1, agent2):
    wins = {}
    wins["1"] = 0
    wins["2"] = 0
    wins["tie"] = 0
    for _ in range(trials):
        g = GameDriver(agent1, agent2)
        winner = g.run()
        if winner == "1":
            break
        wins[winner]+=1
    # for _ in range(trials):
    #     g = GameDriver(agent2, agent1)
    #     winner = g.run()
    #     if winner == "1":
    #         winner = "2"
    #     elif winner == "2":
    #         winner = "1"
    #     wins[winner]+=1
    wins1 = wins["1"]
    wins2 = wins["2"]
    ties = wins["tie"]
    noneloss1 = wins2/trials
    noneloss2 = wins1/trials
    print(f"Player 1 won {wins1} times, losing {noneloss1}% of the time")
    print(f"Player 2 won {wins2} times, losing {noneloss2}% of the time")
    print(f"The game tied {ties} times")

    

        


if __name__ == "__main__":

    # g = GameDriver(RandomAgent, SabotageAgent)
    # g.run()

    agent_tester(500, RandomAgent,SabotageAgent)