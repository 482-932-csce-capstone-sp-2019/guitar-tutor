import math

A4FREQ = 440
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

def getCentsOff(baseFreq, testFreq):
    return 1200 * math.log2(testFreq / baseFreq)

def getNoteIndex(freq):
    centsOffBase = getCentsOff(A4FREQ, freq)
    absCentsOff = abs(centsOffBase)
    absQuarterStepsOff = absCentsOff % 50
    if absQuarterStepsOff == 0:
        return 57
    else:
        if centsOffBase < 0:
            halfStepsOff = -1 * (((absQuarterStepsOff - 1) % 2) + 1)
        else:
            halfStepsOff = ((absQuarterStepsOff - 1) % 2) + 1
    return 57 + halfStepsOff

def getNoteName(freq):
    idx = getNoteIndex(freq)
    nameIdx = idx % 12
    return NOTE_NAMES[nameIdx]