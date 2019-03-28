from pyparsing import *
import fileinput

import os, sys
lib_path = os.path.abspath(os.path.join('..', 'Arduino'))
sys.path.append(lib_path)


from Lights import *

# Parses and creates data structure
def parser(file):

    line = ""
    song = {}
    song["e"] = {}
    song["B"] = {}
    song["G"] = {}
    song["D"] = {}
    song["A"] = {}
    song["E"] = {}

    for string in song:
        for measure in (range(101)):
            song[string][measure] = {}
            for note in (range(80)):
                song[string][measure][note] = {}
                for fret in (range(24)):
                    song[string][measure][note][fret] = False
    print(song)

    # This is going to keep track of the measure we are on. This is just going to keep it organized
    measureCount = {}
    measureCount["e"] = 1
    measureCount["B"] = 1
    measureCount["G"] = 1
    measureCount["D"] = 1
    measureCount["A"] = 1
    measureCount["E"] = 1


    file = lib_path = os.path.abspath(os.path.join('.', 'data/Tabs', file))
    inpt = open(file,"r")
    l = list(inpt.read())
    r = range(len(l))
    rIter = iter(r)
    for i in rIter:
        if l[i] == "e":
            string = "e"
            note = 1
            next(rIter)
        elif l[i] == "B":
            string = "B"
            note = 1
            next(rIter)
        elif l[i] == "G":
            string = "G"
            note = 1
            next(rIter)
        elif l[i] == "D":
            string = "D"
            note = 1
            next(rIter)
        elif l[i] == "A":
            string = "A"
            note = 1
            next(rIter)
        elif l[i] == "E":
            string = "E"
            note = 1
            next(rIter)
        elif l[i] == "|":
            measureCount[string] += 1
        else:
            if l[i].isdigit():
                if l[i+1].isdigit():
                    dig = l[i]
                    next(rIter)
                    dig2 = l[i]
                    dig += dig2
                    fret = int(dig)
                else:
                    fret = int(l[i])
                song[string][measureCount[string]][note][fret] = True
                # print (string + " " + str(measureCount[string]) + " " + str(note) + " " + str(fret) + " " + str(song[string][measureCount[string]][note][fret]))
            note += 1
    return song
