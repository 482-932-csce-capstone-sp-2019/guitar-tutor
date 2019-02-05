from pyparsing import *
import fileinput

import os, sys
a = os.path.abspath(os.path.join('.','Arduino'))
sys.path.append(a)
b = os.path.abspath(os.path.join('.', 'Parsing'))
sys.path.append(b)
c = os.path.abspath(os.path.join('.','Note Recognition, etc'))
sys.path.append(c)

from Lights import *
from Parser import *
from Chords import *

def main():
    
    # Parses and creates data structure.
    while True:
        mode = input("Would you like to learn a chord or play a tab?(Chord/Tab/Quit)")
        mode = mode.lower()
        if mode == "tab":
            song = parser()
            lightGuitar(song)
        elif mode == "chord":
            chords()
        elif mode == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Sorry the input was not understood")
    
main()