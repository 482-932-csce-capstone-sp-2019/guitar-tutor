import serial # you need to install the pySerial :pyserial.sourceforge.net
import time
import binascii

import os, sys
lib_path = os.path.abspath(os.path.join('..', 'Note Recognition, etc'))
sys.path.append(lib_path)

from SoundDriver import NoteRecognizer

a1 = NoteRecognizer()

# used to launch the application without the arduino plugged in
# used mostly for development purposes
noArduinoMode = False

# GUI needs to stay active while a tab is being played
# When the user wants to play a tab, start a thread to do so
doneWithTab = False
def setDoneWithTab(state):
    global doneWithTab
    doneWithTab = state
 

pressed = False

# attempts to find the arduino port
# sets the application to noarduino mode if it cannot be found
def findArduino():
    global noArduinoMode
    possiblePorts = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6']
    arduino = 0
    for p in possiblePorts:
        try :
            arduino = serial.Serial(p, 9600)
            break
        except:
            arduino = 0
    if arduino == 0:
        print('Could not find arduino, starting in GUI only mode')
        noArduinoMode = True

    return arduino

arduino = findArduino()

def onOffFunction(fret, string):
    global noArduinoMode
    # This creates the full binary string we are going to use and converts it to a byte which will light the light.
    light = fret + string
    n = int(light, 2)
    byt = bytes([n])
    if not noArduinoMode:
        arduino.write(byt)

def clearLights(note = -1):
    global doneWithTab
    if doneWithTab:
        pressed = True
    else:
        a1.waitForOnset(note)

    n = int("0",2)
    byt = bytes([n])
    if not noArduinoMode:
        arduino.write(byt)
    return checkBackwards()

def cl(note = -1):
    # Clears all lights
    #a.waitForOnset(note)
    global noArduinoMode

    n = int("0",2)
    byt = bytes([n])
    if not noArduinoMode:
        arduino.write(byt)
    return checkBackwards()

def checkBackwards():
    if pressed == True:
        return -1
    else:
        return 1

def ifDoneKillStream():
    global doneWithTab
    if (doneWithTab):
        cl()
        a1.s.stop()
        exit()

note = 0
measure = 0
fret = 0

def getSongPosition():
    global note
    global measure
    global fret
    return (measure, note, fret)

# Loops through the data structure and lights the appropriate lights.
# this is meant to be run as a thread alongside the actual application
def lightGuitar(song):
    global noArduinoMode
    global doneWithTab
    global note
    global measure
    global fret
    # if the arduino is not connected, just exit
    if (noArduinoMode):
        time.sleep(2)
        exit()
    try:
        a1.s.start()
        onLights = []
        clear = False
        for measure in range(101):
            note = 0
            renderedNote = None
            while note < 80:
                ifDoneKillStream()
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
                    n = clearLights(renderedNote)
                    if (n == -1):
                        a1.s.stop()
                        cl()
                        exit()
                    note += n
                    
                else: 
                    note += 1
        a1.s.stop()
    except KeyboardInterrupt:
        a1.s.stop()
        cl()
    print(a1.correctNotes/a1.totalNotes)
# onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
time.sleep(2) #waiting the initialization...