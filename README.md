# guitartutor
Made in Python 3.6 using the following Open Source Python libraries:

**aubio**

**PySoundCard**

**PySerial**

Designed for use with device produced as part of this project, utilizing an Arduino. See paper for more detail on design of this project and software.

In order to run this software, install all of the above libraries (ideally using a package managment sorftware like pip or conda). Plug the Arduino into COM4 on your device, and feed the audio from the guitar into your computer, setting it to the default recording device. If you wish, you can feed the guitar output through an amplifier before routing it to your machine.

At that point, you can load your Tabs into the "Tabs" folder as ascii data (.txt should be fine). Simply choose tab and type the file name to play through the song. Alternatively, you can play a preloaded chord by choosing chord, then typing the chord name.

run program: Python Main.py
