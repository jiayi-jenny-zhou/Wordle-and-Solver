#!/usr/bin/env python3

from wordle import Player, GameManager
from wordlist import WordList
from scipy.stats import entropy
from information import patterns
from information import *
from wordle import Color
import csv
import math

class Solver(Player):
   

    def __init__(self):
        """
        Initialize the solver.
        """

        self.wordlist = WordList("possible_words.txt")
        self.num_guesses = 0

    def make_guess(self):
        """
        the make_guess function makes a guess.

        Currently, it always guesses "salty". Write code here to improve your solver.
        """
        return "salty"

    def update_knowledge(self, info):
        """
        update_knowledge updates the solver's knowledge with an `info`
        info is an element of the `Information` class. See `information.py`
        """
        print(info)
      
class RandomSolver(Solver):
    
    def make_guess(self):
        ###### print(f"BEFORE guess: {self.wordlist}")
        return self.wordlist.get_random_word()
    
    def update_knowledge(self,info):
        self.wordlist.refine(info)
        ####### print("UPDATE KNOWLEDGE CALLED:")
        ###### print(f"AFTER REFINEMENT{self.wordlist}")
        print(info)
    
    def name():
        return "Random Solver"

class MattParkerSolver(Solver):
    def make_guess(self):
        matt_parker_words = ["gucks", "fjord", "waltz", "nymph", "vibex"]
        if self.num_guesses<5:
            current_guess = self.num_guesses
            self.num_guesses+=1

            return matt_parker_words[current_guess]
        return self.wordlist.get_random_word()
    
    def update_knowledge(self,info):
        self.wordlist.refine(info)
        ###### print(info)
    
    def name():
        return "Matt Parker Solver"


class Entropy():
  
  @staticmethod
  def entropy_pattern_match(guess, word, pattern):
      for (idx,code) in enumerate(pattern):
            if code == Code.hit():
                try:
                    if word[idx] != guess[idx]:
                        return False
                except e: #originally e
                    print(word, idx, guess)
                    raise e
            if code == Code.miss():
                if guess[idx] in word:
                    return False
            if code == Code.mem():
                if guess[idx] not in word \
                   or guess[idx] == word[idx]:
                    return False
      return True

  @staticmethod
  def calculate_pattern_probability(guess, pattern, wordlist):
      total_words = len(wordlist)
      probable_words = 0
      
      # # ####
      # string = ""
      # for (i,code) in enumerate(pattern):
      #     if code == Code.hit():
      #         string += Color.green(guess[i])
      #     elif code == Code.mem():
      #         string += Color.yellow(guess[i])
      #     else:
      #         string += guess[i]
      # print(f"guess: {guess},  pattern:{string} ")
      # things_working = [] 
      ###############

      for word in wordlist:
          if Entropy.entropy_pattern_match(guess, word, pattern) == True:
              
              #############
              # things_working.append(word)
              # #######
              probable_words+=1
          
      # print(f"words working: {things_working}, probable words: {probable_words}") ##########


      return float(probable_words)/total_words
  
  @staticmethod
  def calculate_entropy(guess, wordlist):
      guess_entropy = 0.0
      for pattern in patterns():
          
          pattern_probability = Entropy.calculate_pattern_probability(guess, pattern , wordlist)

          # print(pattern_probability)
          # ############
          # string = ""
          # for (i,code) in enumerate(pattern):
          #     if code == Code.hit():
          #         string += Color.green(guess[i])
          #     elif code == Code.mem():
          #         string += Color.yellow(guess[i])
          #     else:
          #         string += guess[i]
          # print(f"{pattern_probability}, {string}")
          # ###############


          info_gained = -1.0 * math.log(pattern_probability+.00000000000000000000000000001,2)
          pattern_entropy = pattern_probability * info_gained
          guess_entropy += pattern_entropy
      return guess_entropy
  
  @staticmethod
  def max_entropy_word(wordlist):
      best_word = None
      highest_entropy = None
      # f = open(r"first_guess_entropies.txt","w")

      for word in wordlist:
          word_entropy = Entropy.calculate_entropy(word, wordlist)


          # f.write(f"{word_entropy} {word}\n")

          # print(f"{word_entropy} {word}")

          if highest_entropy == None:
              highest_entropy = word_entropy
              best_word = word
          elif word_entropy > highest_entropy:
              highest_entropy = word_entropy
              best_word = word
      
      # print(f"bestword: {best_word}")
      return best_word
  
  @staticmethod
  def tail_match(word, refined_word):
      pat = Pattern(refined_word, word)
      return str(pat)
        
  @staticmethod
  def ound_entropy_max(wordlist):
      total_words = WordList("possible_words.txt")
      best_word = None
      highest_entropy = None
      print(wordlist)

      for word in total_words:
          patterns = []
          patterns_set = set()
          #calculating occurances
          for refined_word in wordlist:
              pattern = Entropy.tail_match(word,refined_word)
              
              patterns.append(pattern)
              patterns_set.add(pattern)
          
          #calculating probability
          word_entropy = 0.0

          for pattern in patterns_set:
              pattern_probability = float(patterns.count(pattern))/len(patterns)
             
              word_entropy+= pattern_probability* -1.0 * math.log(pattern_probability+.00000000000000000000000000001,2)
          print(f"word entropy {word_entropy}")
          if highest_entropy == None:
              highest_entropy = word_entropy
              best_word = word
                      
          elif word_entropy > highest_entropy:
              print("here")
              highest_entropy = word_entropy
              best_word = word

      return (best_word, highest_entropy)
          
                
  @staticmethod
  def max_entropy_second_word_calculator(filename):
      total_words = WordList(filename)
      best_words = {}
      guess1 = "tares"
      for pattern in patterns():
          refined_wordlist = []
          for test_word in total_words:
              if Entropy.entropy_pattern_match(guess1,test_word, pattern):
                  refined_wordlist.append(test_word)

          print(refined_wordlist)
          best_word = Entropy.max_entropy_word(refined_wordlist)
          best_words[str(pattern)] = best_word
          print(f"{guess1}, {str(pattern)}: {best_word}")
      
      with open("best_second_guess_w.csv", "w") as f:
          f.write("key,best_word")
          for key in best_words.keys():
              f.write(f"{key},{best_words[key]}\n")
              
      print(best_words)
      
      
class EntropySolver(Solver):
    
    def __init__(self):
        """
        Initialize the solver.
        """

        self.wordlist = WordList("possible_words.txt")
        self.num_guesses = 0
        self.lastpattern = ""


    def make_guess(self):
        refined_entropy = None
        if self.num_guesses==0:
            self.num_guesses+=1
            # print("lares")
            return "tares" 
        elif self.num_guesses==1:
            self.num_guesses+=1
            second_words = {}
            with open("best_second_guess_w.csv", "r") as f:
                data = csv.reader(f)
                second_words = {rows[0]:rows[1] for rows in data}
                # print(second_words)
            return second_words[self.lastpattern]
        # elif self.num_guesses ==2:
        #     self.num_guesses+=1 
        # elif self.num_guesses ==3:
        #     self.num_guesses+=1
        # elif self.num_guesses>=4:
        #     self.num_guesses+=1
        #     if(len(self.wordlist)==1):
        #         return self.wordlist[0]
        #     refined_entropy = Entropy.max_entropy_word(self.wordlist)
        #     ound_entropy = Entropy.ound_entropy_max(self.wordlist)
            
        #     if (refined_entropy[1]<ound_entropy[1]):
        #         return ound_entropy[0]
        #     else:
        #         return refined_entropy[0]
        
        return Entropy.max_entropy_word(self.wordlist)
        
    
    def update_knowledge(self, info):
        self.wordlist.refine(info)
        self.lastpattern = info.return_pattern()


    def name():
        return "Entropy Solver"
        
            
def main():
    solver  = Solver()
    manager = GameManager(solver)
    n_guess = manager.play_game()
    print("you found the word in", n_guess, "guesses")

if __name__ == "__main__": main()
