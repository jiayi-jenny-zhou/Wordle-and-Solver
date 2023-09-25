#!/usr/bin/env python3

from random import choice

from solver import *
from information import *
from wordlist import WordList


class Wordle():
    """The Wordle Game State

    this class manages and processes player guesses
    """

    def __init__(self, word = None):
        """Creates a Wordle Game

        The optional `word` argument specifies the game word. If no word is
        given, a random word is drawn from the word list.
        """
        self.guesses = []
        if word is None:
            self.word = WordList("possible_words.txt").get_random_word() #HERE RANDOM
            # self.word = "found"
        else:
            self.word = word

        print(f"word is: {self.word}")#####

    def string_guess(self, guess):
        """Converts a guess to a colorized string corresponding to the information content."""
        return str(Information(goal_word = self.word, guess = guess))

    def __str__(self):
        """
        converts the set of guessed words to a string
        """
        return "-----\n" \
            +  "\n".join(map(self.string_guess, self.guesses)) \
            +   "\n-----\n"

    def guess(self, guess):
        """A guess is made and information about the guess is returned"""
        assert guess is not None
        self.guesses.append(guess)
        # print(guess) ###### HERE
        return Information(goal = self.word, guess = guess)

    def is_word(self, guess):
        """Checks whether the guess is itself the word"""
        return guess == self.word

class Player():
    """Represents a human wordle player.

    Records a numeric count of the guesses and allows the human player to make
    guesses.
    """

    def __init__(self):
        """Initialize the player"""
        self.num_guesses = 0

    def make_guess(self):
        """returns a string guess

        For the human `Player`, the guess is read from the user's input. If the
        user's input is ill-formed (i.e.) not a sequence of 5 characters,
        `make_guess` prompts the user again and again until it is.
        """
        guess = ""
        while len(guess) != 5:
            guess = input("> ")
            guess = guess.strip()
        self.num_guesses += 1
        return guess

    def update_knowledge(self, info):
        """updates the knowledge state with `info`

        For the human `Player` the `info` is simply printed to the CLI to update
        the human about the quality of their guess
        """
        print(info)



class GameManager():
    """The GameManager runs the main control loop of the Wordle game """

    def __init__(self, player):
        """starts a game with one `player`"""
        self.wordle = Wordle()
        self.player = player

    def play_game(self):
        """starts the main game loop.

        The loop solicits guesses from self's player and passes them to self's
        wordle instance. It then conveys the success/fail info back to self's player.
        The loop continues until the player guesses the correct word.
        """
        guess = ""
        num_guesses = 0
        while not self.wordle.is_word(guess):
            guess = self.player.make_guess()
            num_guesses += 1
            info = self.wordle.guess(guess)
            self.player.update_knowledge(info)
        return num_guesses

def solver_tester(n,solver):
    total_guesses = 0
    max_guess = 0
    min_guess = 13000
    for _ in range(n):
        num_guesses = 0
        g = GameManager(solver())

        num_guesses = g.play_game()
        total_guesses+=num_guesses
        max_guess = max(max_guess, num_guesses)
        min_guess = min(min_guess, num_guesses)
        print("you found the word in", num_guesses, "guesses")

    average_guess = float(total_guesses)/n
    print(f"In {n} tests, {solver.name()} had a high of {max_guess}, a low of {min_guess}, and averaged {average_guess} guesses.")
    

def main():
    # g = GameManager(EntropySolver())
    # num_guesses = g.play_game()
    # print("You guessed the word in", num_guesses, "guesses!")

    # solver_tester(100, RandomSolver)
    # solver_tester(100, MattParkerSolver)
    solver_tester(4000, EntropySolver)

    ###################33
    # pattern_list = patterns()
    # pattern_test = pattern_list[0]
    # guess_test = "molly"
    # word_test = "reddy"
    # string = ""
    # for (i,code) in enumerate(pattern_test):
    #     if code == Code.hit():
    #         string += Color.green(guess_test[i])
    #     elif code == Code.mem():
    #         string += Color.yellow(guess_test[i])
    #     else:
    #         string += guess_test[i]
    # matching_test = Entropy.entropy_pattern_match(guess_test,word_test,pattern_test)
    # print(f" for {string}, {word_test} returned {matching_test}")
    # ##########################

    # print(Entropy.max_entropy_word(WordList("words.txt")))

    # Entropy.max_entropy_second_word_calculator("words.txt")





if __name__ == "__main__": main()
