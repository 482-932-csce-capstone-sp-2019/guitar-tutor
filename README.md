# guitartutor
Made in Python 3.7 using the following Open Source Python libraries:

**aubio**

**PySoundCard**

**PySerial**

**Kivy**

**MIDO**

**python-rtmidi**

**Pyaudio**

Install the following for midi recognition
 
FL STUDIO ASIO

LOOPBE INTERNAL MIDI

JAM ORIGIN
 
Designed for use with device produced as part of this project, utilizing an Arduino. See paper for more detail on design of this project and software.

In order to run this software, install all of the above libraries (ideally using a package managment sorftware like pip or conda). 

Plug the Arduino into COM4 on your device, and feed the the quater inch jack to usb wire into the guitar and the machine running the software.

Make sure LOOPBE is not muted, jam origin is on and the following setting are set in jam origin,

Driver = FL STUDIO ASIO, and INPUT = LOOPBE INTERNAL MIDI

run program: Python guitartutor.py
