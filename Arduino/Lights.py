import serial # you need to install the pySerial :pyserial.sourceforge.net
import time
import binascii

import os, sys
lib_path = os.path.abspath(os.path.join('..', 'Note Recognition, etc'))
sys.path.append(lib_path)

from SoundDriver import NoteRecognizer

a1 = NoteRecognizer()


pressed = False

def findArduino():
    possiblePorts = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6']
    arduino = 0
    for p in possiblePorts:
        try :
            arduino = serial.Serial(p, 9600)
            break
        except:
            arduino = 0
    if arduino == 0:
        print('Could not find arduino, exiting')
        exit()
    return arduino

arduino = findArduino()

def onOffFunction(fret, string):
    # This creates the full binary string we are going to use and converts it to a byte which will light the light.
    light = fret + string
    #print(light)
    n = int(light, 2)
    byt = bytes([n])
    arduino.write(byt)

def clearLights(note = -1):
    # Clears all lights
    a1.waitForOnset(note)
    #input("Wait")
    #print("test")

    n = int("0",2)
    byt = bytes([n])
    arduino.write(byt)
    return checkBackwards()

def cl(note = -1):
    # Clears all lights
    #a.waitForOnset(note)
    #input("Wait")
    #print("test")

    n = int("0",2)
    byt = bytes([n])
    arduino.write(byt)
    return checkBackwards()

def checkBackwards():
    if pressed == True:
        return -1
    else:
        return 1

# Loops through the data structure and lights the appropriate lights.
def lightGuitar(song):
    a1.s.start()
    onLights = []
    clear = False
    for measure in range(101):
        note = 0
        renderedNote = None
        while note < 80:
            renderedNote = None
            for fret in range(24):
                if song["e"][measure][note][fret] == True:
                    onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(6))
                    clear = True
                    if renderedNote != None:
                        renderedNote = False
                    else:
                        renderedNote = 52 + fret
                if song["B"][measure][note][fret] == True:
                    onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(5))
                    clear = True
                    if renderedNote != None:
                        renderedNote = False
                    else:
                        renderedNote = 47 + fret
                if song["G"][measure][note][fret] == True:
                    onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(4))
                    clear = True
                    if renderedNote != None:
                        renderedNote = False
                    else:
                        renderedNote = 43 + fret
                if song["D"][measure][note][fret] == True:
                    onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(3))
                    clear = True
                    if renderedNote != None:
                        renderedNote = False
                    else:
                        renderedNote = 38 + fret
                if song["A"][measure][note][fret] == True:
                    onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(2))
                    clear = True
                    if renderedNote != None:
                        renderedNote = False
                    else:
                        renderedNote = 33 + fret
                if song["E"][measure][note][fret] == True:
                    onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(1))
                    clear = True
                    if renderedNote != None:
                        renderedNote = False
                    else:
                        renderedNote = 28 + fret					
            if clear == True:
                clear = False
                note += clearLights(renderedNote)
            else: 
                note += 1
    #print("You got %f of the notes correct." % (float(a.correctNotes)/float(a.totalNotes)))
    a1.s.stop()
# onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
time.sleep(2) #waiting the initialization...