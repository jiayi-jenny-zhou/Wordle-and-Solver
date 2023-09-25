#!/usr/bin/env python3

from random import choice

class WordList():
    """
    The wordlist class is a wrapper for a list of words.

    """

    def __init__(self, word_file = "possible_words.txt", given_words = None):
        """construct a list of words by reading from `word_file`

        """
        if given_words is None:
            self.words = []
            with open(word_file) as fp:
                self.words = fp.readlines()
            self.words = [w.strip() for w in self.words]
        else:
            self.words = given_words

    def get_random_word(self):
        """returns a random word from the set of words"""
        return choice(self.words)

    def __str__(self):
        return str(self.words)

    def __contains__(self, word):
        return word in self.words

    def __iter__(self):
        return self.words.__iter__()

    def __len__(self):
        return len(self.words)

    def refine(self, information):
        """updates the words to be consistent with the `information`"""
        words = []
        for word in self.words:
            if information.matches(word):
                words.append(word)
        self.words = words

    def matching(self, pattern, guess):
        """returns a list of words that could've produced `pattern` in response to `guess`"""
        return [word
                for word in self.words
                if pattern.matches(guess, word)]
