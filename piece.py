import random
#!/usr/bin/env python3

from itertools import cycle
    
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
        self.attribute_str = ''.join([str(attribute) for attribute in self.attribute_list])

    def get_attribute_list(self):
        return self.attribute_list

    def get_attribute_str(self):
        return self.attribute_str
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