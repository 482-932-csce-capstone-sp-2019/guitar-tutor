import serial # you need to install the pySerial :pyserial.sourceforge.net
import time
import binascii
import sys

sys.path.insert(0, 'C:/School/CSCE 482/GUITARTUTOR/Arduino')

from Lights import *

ac = "e|-|\nB|-|\nG|2|\nD|2|\nA|2|\nE|-|" , "A"
a7c = "e|-|\nB|-|\nG|2|\nD|-|\nA|2|\nE|-|", "A7"
amc = "e|-|\nB|-|\nG|2|\nD|2|\nA|1|\nE|-|", "Am"
am7c = "e|-|\nB|-|\nG|2|\nD|-|\nA|1|\nE|-|", "Am7"
amaj7c = "e|-|\nB|-|\nG|2|\nD|1|\nA|2|\nE|-|", "Amaj7"
bfc = "e|-|\nB|1|\nG|3|\nD|3|\nA|3|\nE|-|", "Bb"
b7c = "e|-|\nB|2|\nG|1|\nD|2|\nA|-|\nE|2|", "B7"
bmc = "e|-|\nB|2|\nG|4|\nD|4|\nA|3|\nE|-|", "Bm"
cc = "e|-|\nB|3|\nG|2|\nD|-|\nA|1|\nE|-|", "C"
c7c = "e|-|\nB|3|\nG|2|\nD|3|\nA|1|\nE|-|", "C7"
cmaj7c = "e|-|\nB|2|\nG|4|\nD|4|\nA|3|\nE|-|", "Cmaj7"
dc = "e|-|\nB|-|\nG|-|\nD|2|\nA|3|\nE|2|", "D"
d7c = "e|-|\nB|-|\nG|-|\nD|2|\nA|1|\nE|2|", "D7"
dmc = "e|-|\nB|-|\nG|-|\nD|2|\nA|3|\nE|1|", "Dm"
dm7c = "e|-|\nB|-|\nG|-|\nD|2|\nA|1|\nE|1|", "Dm7"
dmaj7c = "e|-|\nB|-|\nG|-|\nD|2|\nA|2|\nE|2|", "Dmaj7"
ec = "e|-|\nB|2|\nG|2|\nD|1|\nA|-|\nE|-|", "E"
e7c = "e|-|\nB|2|\nG|-|\nD|1|\nA|-|\nE|-|", "E7"
emc = "e|-|\nB|2|\nG|2|\nD|-|\nA|-|\nE|-|", "Em"
em7c = "e|-|\nB|2|\nG|-|\nD|-|\nA|-|\nE|-|", "Em7"
fc = "e|1|\nB|3|\nG|3|\nD|2|\nA|1|\nE|1|", "F"
fmaj7c = "e|-|\nB|-|\nG|3|\nD|2|\nA|1|\nE|-|", "Fmaj7"
gc = "e|3|\nB|2|\nG|-|\nD|-|\nA|-|\nE|3|", "G"
g7c = "e|3|\nB|2|\nG|-|\nD|-|\nA|-|\nE|1|", "G7"
def chords(chord):
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
        cmaj7()
    elif chord == "d":
        d() 
    elif chord == "dm":
        dm()
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
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))

def a7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def am():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def am7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def amaj7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def bf():
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))

def b7():
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(6))

def bm():
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(4), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(4), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))

def c():
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def c7():
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def cmaj7():
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def d():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(6))

def d7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(6))

def dm():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(6))

def dm7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(6))

def dmaj7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(6))

def e():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def e7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def em():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def em7():
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def f():
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(6))

def fmaj7():
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(6))

def g():
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(6))

def g7():
    onOffFunction('{0:05b}'.format(3), '{0:03b}'.format(1))
    onOffFunction('{0:05b}'.format(2), '{0:03b}'.format(2))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(3))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(4))
    onOffFunction('{0:05b}'.format(0), '{0:03b}'.format(5))
    onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(6))

#chords()