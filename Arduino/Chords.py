import serial # you need to install the pySerial :pyserial.sourceforge.net
import time
import binascii
import sys

sys.path.insert(0, 'C:/School/CSCE 482/GUITARTUTOR/Arduino')

from Lights import *

def chords():
    chord = input("Choose a chord: ")
    chord.lower()
    if chord == "a":
        a()
    elif chord == "a7":
        a7()
    elif chord == "am":
        am()
    elif chord == "am7":
        am7()
    elif chord == "amaj7":
        amaj7()
    elif chord == "bf":
        bf()
    elif chord == "b7":
        b7()
    elif chord == "bm":
        bm()
    elif chord == "c":
        c()
    elif chord == "c7":
        c7()
    elif chord == "cmaj7":
        c()
    elif chord == "d":
        d() 
    elif chord == "d7":
        d7()
    elif chord == "dm7":
        dm7()
    elif chord == "dmaj7":
        dmaj7()
    elif chord == "e":
        e()
    elif chord == "e7":
        e7()
    elif chord == "em":
        em()
    elif chord == "em7":
        em7()
    elif chord == "f":
        f()
    elif chord == "fmaj7":
        fmaj7()
    elif chord == "g":
        g()
    elif chord == "g7":
        g7()
    else:
        "Chord not known"

def a():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))

def a7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))

def am():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))

def am7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))

def amaj7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))

def bf():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))

def b7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def bm():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(4), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(4), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def c():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))

def c7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))

def cmaj7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))

def d():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))

def d7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))

def dm():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))

def dm7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))

def dmaj7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))

def e():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def e7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def em():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def em7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def f():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(4))

def fmaj7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(4))

def g():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(6))

def g7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(6))

#chords()