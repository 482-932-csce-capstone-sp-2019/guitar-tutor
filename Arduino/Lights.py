import serial # you need to install the pySerial :pyserial.sourceforge.net
import time
import binascii

import os, sys
lib_path = os.path.abspath(os.path.join('..', 'Note Recognition, etc'))
sys.path.append(lib_path)

from SoundDriver import NoteRecognizer, doneWithTab, setDoneWithTab, getDoneWithTab

a1 = NoteRecognizer()

# used to launch the application without the arduino plugged in
# used mostly for development purposes
noArduinoMode = False

# GUI needs to stay active while a tab is being played
# When the user wants to play a tab, start a thread to do so

pressed = False

lastScore = ''


# attempts to find the arduino port
# sets the application to noarduino mode if it cannot be found
def findArduino():
    global noArduinoMode
    possiblePorts = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6']
    arduino = 0
    for p in possiblePorts:
        try :
            arduino = serial.Serial(p, 9600)
            print(arduino)
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

def clearLights(note = []):
    out = None
    print("Note length is:", len(note))
    if getDoneWithTab():
        pressed = True
    else:
        out = a1.waitForOnset(note)
      
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
    #doneWithTab
    if (getDoneWithTab()):
        cl()
        a1.port.close()
        #a1.s.stop()
        exit()

note = 0
measure = 0
fret = 0

def getSongPosition():
    global note
    global measure
    global fret
    return (measure, note, fret)


def scorePush(filepath, scores):
    i = 0
    with open(filepath, 'w+') as filehandle:  
        filehandle.writelines("%s\n" % score for score in scores)
        if i == 10:
            return
        i += 1
# Loops through the data structure and lights the appropriate lights.
# this is meant to be run as a thread alongside the actual application
def lightGuitar(song, tab_name):
    a1.correctNotes = 0
    a1.totalNotes = 0 
    a1.incorrectNotes = 0
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
        #a1.s.start()
        onLights = []
        clear = False
        for measure in range(101):
            note = 0
            renderedNote = []
            while note < 80:
                ifDoneKillStream()
                renderedNote = []
                for fret in range(24):
                    if song["e"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(6))
                        clear = True
                        renderedNote.append(65 + fret)
                    if song["B"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(5))
                        clear = True
                        renderedNote.append(60 + fret)
                    if song["G"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(4))
                        clear = True
                        renderedNote.append(55 + fret)
                    if song["D"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(3))
                        clear = True
                        renderedNote.append(50 + fret)
                    if song["A"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(2))
                        clear = True
                        renderedNote.append(45 + fret)
                    if song["E"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(1))
                        clear = True
                        renderedNote.append(40 + fret)
                if clear == True:
                    clear = False
                    n = clearLights(renderedNote)
                    if (n == -1):
                        a1.port.close()
                        #print("Die")
                        cl()
                        exit()
                    note += n
                    
                else: 
                    note += 1
        #print("You got %f of the notes correct." % (float(a.correctNotes)/float(a.totalNotes)))
        #a1.s.stop()
    except KeyboardInterrupt:
        a1.port.close()
        cl()
    #Score is total notes divided by number of notes played
    curScore = a1.correctNotes/(a1.correctNotes + a1.incorrectNotes)
    lastScore = str(curScore)
    print("Score: " + str(curScore))
    #Get score file for current song or create it
    fileName = os.path.abspath(os.path.join('.', 'Scores/', (tab_name + '.txt')))
    scores = []
    # open file and read the content in a list
    #read in current scores
    with open(fileName, 'r+') as filehandle:  
        scores = [float(score.rstrip()) for score in filehandle.readlines()]
    scores.append(curScore)
    scores = sorted(scores)
    
    scorePush(fileName, scores)
    

practiceScore = 0

def getPracticeScore():
    global practiceScore
    return practiceScore

def resetPracticeScore():
    global practiceScore
    practiceScore = 0

def addToPracticeScore(score):
    global practiceScore
    practiceScore += score


# Loops through the data structure and lights the appropriate lights.
# this is meant to be run as a thread alongside the actual application
# This function is identical to LightGuitar but is only meant to be used for the fingering practice game
def lightGuitarPractice(song, tab_name):
    a1.correctNotes = 0
    a1.totalNotes = 0 
    a1.incorrectNotes = 0
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
        #a1.s.start()
        onLights = []
        clear = False
        for measure in range(101):
            note = 0
            renderedNote = []
            while note < 80:
                ifDoneKillStream()
                renderedNote = []
                for fret in range(24):
                    if song["e"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(6))
                        clear = True
                        renderedNote.append(65 + fret)
                    if song["B"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(5))
                        clear = True
                        renderedNote.append(60 + fret)
                    if song["G"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(4))
                        clear = True
                        renderedNote.append(55 + fret)
                    if song["D"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(3))
                        clear = True
                        renderedNote.append(50 + fret)
                    if song["A"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(2))
                        clear = True
                        renderedNote.append(45 + fret)
                    if song["E"][measure][note][fret] == True:
                        onOffFunction('{0:05b}'.format(fret), '{0:03b}'.format(1))
                        clear = True
                        renderedNote.append(40 + fret)
                if clear == True:
                    clear = False
                    n = clearLights(renderedNote)
                    if (n == -1):
                        a1.port.close()
                        #print("Die")
                        cl()
                        exit()
                    note += n
                    
                else: 
                    note += 1
        #print("You got %f of the notes correct." % (float(a.correctNotes)/float(a.totalNotes)))
        #a1.s.stop()
    except KeyboardInterrupt:
        a1.port.close()
        cl()
    curScore = a1.correctNotes/(a1.correctNotes + a1.incorrectNotes)
    addToPracticeScore(curScore)
    global last_score
    last_score = curScore
    # print("Score: " + str(curScore))
    # fileName = os.path.abspath(os.path.join('.', 'Scores/', (tab_name + '.txt')))
    # scores = []
    # # open file and read the content in a list
    # with open(fileName, 'r+') as filehandle:  
    #     scores = [float(score.rstrip()) for score in filehandle.readlines()]
    # scores.append(curScore)
    # scores = sorted(scores)
    # with open(fileName, 'w+') as filehandle:  
    #     filehandle.writelines("%s\n" % score for score in scores)            
# onOffFunction('{0:05b}'.format(1), '{0:03b}'.format(3))
time.sleep(2) #waiting the initialization...