'''
This is a prototype of our guitar tutoring app.

The app is implemented in Kivy and python 3.

Contributions: 
Gerardo Mares II
Noe Balli IV
Hunter Stewart
Jacob Jackson

Sources:

Tuner:
	Credits: 
		GitHub user handles: mzucker, michniewicz
		URL: https://github.com/michniewicz/python-tuner/graphs/contributors

'''

# import libraries 
import builtins
import random
import time
import threading
import os
import glob
import re
import numpy as np
import pyaudio
import threading
import time
import sys
import shutil

# import  directories for file reading
from os.path import dirname, join

# imports from kivy to get an working app
from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView


# Import folders with helper functions
a = os.path.abspath(os.path.join('.','Arduino'))
sys.path.append(a)
b = os.path.abspath(os.path.join('.', 'Parsing'))
sys.path.append(b)
c = os.path.abspath(os.path.join('.', 'Note Recognition, etc'))
sys.path.append(c)
d = os.path.abspath(os.path.join('.', 'data'))
sys.path.append(d)

from Lights import *
from Parser import *
from chordParser import * 
from Chords import *
from SoundDriver import setDoneWithTab
from cleanTab import cleanTab

# need to reference the thread for tab playing in multiple functions
# made it a global to reflect this
t = threading.Thread()

# lock used to protect the challenge going variable in the app
challengeGoingLock = threading.Lock()

# global for stopping the chord game
playingGame = False

# global that is set when a tab starts
startedATab = False

# global so checking if tuner is turned on or off
Done_Tuning = False

# global for checking is a chord has been played
practiceChordClock = 0


# gets a random chord name from a list of all implemented chords for chord game
def getRandomChord():
	possibleChords = [ac,a7c,amc,am7c,amaj7c,bfc,b7c,bmc,cc,c7c,cmaj7c,dc,d7c,dmc,dm7c,dmaj7c,ec,e7c,emc,em7c,fc,fmaj7c,gc,g7c]
	return random.choice(possibleChords)

# this is the widget that runs on the one more note screen
# it just checks if the program is still listening for notes		
class OneMoreNoteWidget(Widget):
	oneMoreNoteClock = 0
	def __init__(self, **kwargs):
		super(OneMoreNoteWidget, self).__init__(**kwargs)
		self.oneMoreNoteClock = Clock.schedule_interval(self.update, 1/60.)
	
	def update(self, *args):
		if not t.isAlive() and app.index == app.oneMoreNoteIdx:
			app.go_screen(app.homeScreenIdx)


# Loading screen widget for loading tab file
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

# This is our main application that holds all screens
class GuitarApp(App):
	# the string name of the app the system is currently playing
	currentlyPlayingTab = StringProperty()
	# a boolean that displays whether or not the user is still playing the chord practice game
	challengeGoing = BooleanProperty(False)
	# Use index to cycle through screens
	index = NumericProperty(-1)
	# Keep all screens in a list to access later
	screen_names = ListProperty([])
	# Title of current screen
	current_title = StringProperty()

	# Used in chord library
	# Displays the given chord on the guitar
	def displayChord(self, chord):
		cl()
		chords(chord)
	
	def build(self):
		# Title of window
		self.title = 'Guitar Tutor'
		# Initialize the list of screen that app has
		self.screens = {}
		# Add screens to the list
		self.available_screens = ["HomeScreen", "ChordLibrary",
			"TabLibrary", "AddTab", "Challenge", "Tuner", "PlayingTab", 
			"OneMoreNote", "Scoreboard", "ScoreboardChord"]
		self.homeScreenIdx = 0
		self.chordLibraryIdx = 1
		self.tabLibraryIdx = 2
		self.addTabIdx = 3
		self.challengeIdx = 4
		self.tunerIdx = 5
		self.playingTabIdx = 6
		self.oneMoreNoteIdx = 7
		self.scoreboardIdx = 8
		self.scoreboardChordIdx = 9
		# Remember names of screens, used for loading files
		self.screen_names = self.available_screens
		# Get current directory
		curdir = dirname(__file__)
		# Re-fill available screens with the path to each screen
		self.available_screens = [join(curdir, 'data', 'screens',
			'{}.kv'.format(fn).lower()) for fn in self.available_screens]
		# Initialize first screen (index 0)
		self.go_screen(self.homeScreenIdx)

	def clear(self):
		cl()	
	
	#Testing with showing source code
	def toggle_tab_viewer(self,*tab_name):
		height = self.root.height * .5
		
		Animation(height=height, d=.3, t='out_quart').start(
			self.root.ids.sv)
		
		self.update_tab_viewer(tab_name[0])

	def quit_tab_viewer(self, *args):
		Animation(height=0, d=.3, t='out_quart').start(self.root.ids.sv)
		
	def read_tab(self, *tab_name):
		fn = self.available_screens[self.index]
		curdir = dirname(__file__)
		fn = tab_name[0].text
		fn = join(curdir, 'data', 'tabs', '{}.txt'.format(fn))

		with open(fn) as fd:
			# get length of a single line to get horizontal scroll
			line = fd.readline()
			# 9.1 is a magic number used to get the right width for horizontal scrolling
			self.root.ids.sourcecode.width = 9.1 * len(line)
			
			# reset cursor for reading
			fd.seek(0)			
			# return actual tab to display
			return fd.read()
	
	def update_tab_viewer(self, *args):
		self.root.ids.sourcecode.text = self.read_tab(args[0])
		self.root.ids.sv.scroll_y = 1
		self.root.ids.sv.scroll_x = 0
	
	# tell application to switch to another screen
	def go_screen(self, idx):
		cl()
		if(t.isAlive() and self.index != self.oneMoreNoteIdx and self.index != self.tabLibraryIdx and self.index != self.challengeIdx):
			self.index = self.oneMoreNoteIdx
			self.root.ids.sm.switch_to(self.load_screen(self.oneMoreNoteIdx), direction="left")
			return
		elif(t.isAlive() and self.index == self.oneMoreNoteIdx):
			return
		if(self.index != idx):
			self.index = idx
			self.root.ids.sm.switch_to(self.load_screen(idx), direction="left")

	# returns a screen
	# might be modified to search for next screen... maybe
	def load_screen(self, index):
		if index in self.screens:
			return self.screens[index]
		screen = Builder.load_file(self.available_screens[index])
		self.screens[index] = screen
		return screen
		
	def start_tuner(*args):
		set_Done_Tuning(False)
		t1 = threading.Thread(target = tune)
		t1.daemon = True
		t1.start()
	
	def stop_tuner(*args):
		set_Done_Tuning(True)
		
	# serves as a loading screen when starting tuner
	def do_tuning(self):
		tuner_page = self.screens[5].layout
		tuner_page.clear_widgets()
		
		loadingtext = Label()
		loadingtext.text = 'Starting Tuner...'
		loadingtext.font_size = '20dp'
		loadingtext.bind(on_release = app.start_tuner)
		tuner_page.add_widget(loadingtext)
		
	# this is the front end for the tuner, it displays whether the user should tune up or down
	# along with other helpful metrics
	def update_tuner(self, note_name, cents):
		tuner_page = self.screens[5].layout
		tuner_page.clear_widgets()
		
		guide = Label()
		label = Label()
		title = Label()
		
		guide.text = "E2 A2 D3 G3 B3 E4"
		guide.font_size = '25dp'
		
		cents = cents * 100
		
		# text to tune up or down
		tuner_text = ''
		label.color = [1, 0, 0, 1]
		
		if np.greater(-10.0,cents):
			tuner_text = 'Tune Up \n{:+.2f} cents'.format(cents)
		
		if np.greater(cents, 10.0):
			tuner_text = 'Tune Down \n{:+.2f} cents'.format(cents)
			
		if tuner_text == '':
			tuner_text = 'In Tune \n{:+.2f} cents'.format(cents)
			label.color = [0, 1, 0, 1]
		
		title.text = tuner_text
		title.font_size = '25dp'
		label.text = note_name
		label.font_size = '100dp'
		
		tuner_page.add_widget(guide)
		tuner_page.add_widget(title)
		tuner_page.add_widget(label)
	
	# Dynamically make buttons for all tab files in the tabs folder
	def load_tabs(self, tab_page):
		# delete all previous buttons!
		# this way we don't duplicate buttons
		tab_page.clear_widgets()

		# Grab all tab files using glob
		path = 'data/tabs/*.txt'
		files = sorted(glob.glob(path))
		# array of file names so we can name each button
		file_names = []
		
		# Couldn't figure out how to make the app scrollable
		# Decided to just prevent the tabs from overflowing
		if len(files) > 25:
			errbutton = Button()
			errbutton.text = "25 Tab Maximum Reached"
			tab_page.add_widget(errbutton)
			return
		
		# strip the directory path and only store the file name. Strip .txt too
		for name in files:
			# \\ match a literal \
			# ( start a capturing group
			# [^]. match anything except a .
			# * zero or more of the previous
			# ) close the capturing group
			# \. match a literal .
			file_names.append(re.findall(r'\\([^.]*)\.', name)[0])
		
		# Sort names just in case. Now index in files and file_names are the same!
		# We can use this to open the correct file
		file_names = sorted(file_names)

		# make score files for each tab file, append if already exists
		for name in file_names:
			fileName = os.path.abspath(os.path.join('.', 'Scores/', (name + '.txt')))
			f = open(fileName, 'a')
			f.close()
		
		# Dynamically create a button for each tab
		for tab in range(len(file_names)):
			# Declare button
			button = Button()
			# Configure text of button
			button.text = file_names[tab]
			# Configure id. To be used when loading tab files
			button.id = files[tab]
			# Configure size of button
			button.size_hint = (.2, .2)
			# Add function to button
			button.bind(on_release = play_tab)
			button.bind(on_release = self.toggle_tab_viewer)
			# Add button!
			tab_page.add_widget(button)
	
	# called when the user wants to stop playing the tab midway through
	def stopTab(self):
		if (not getDoneWithTab()):
			setDoneWithTab(True)
			cl()
			global startedATab
			startedATab = False
			app.go_screen(self.oneMoreNoteIdx)

	# this function stops the chord practice game
	# it takes care of all the cleanup for the game
	def stopChord(self):
		global startedATab
		global challengeGoingLock
		self.setPlayingChallenge(False)
		startedATab = False
		setDoneWithTab(True)
		cl()
		self.go_screen(self.scoreboardChordIdx)
		app.screens[self.scoreboardChordIdx].ids.LastScore.text = getPracticeScore()
		resetPracticeScore()

	# returns the top 5 scores on the current song
	def get5Scores(self):
		file = open("Scores/" + self.currentlyPlayingTab + ".txt")
		scores = []
		for line in file:
			scores.append(line[:-1])
		scores.sort(reverse=True)
		if len(scores) < 5:
			for i in range(5 - len(scores)):
				scores.append('')
		return scores[:5]

	# returns the latest score returned by the system
	def getLastScore(self):
		return getTheLastScore()

	# this function is slightly different from the original play tab which is meant to play an entire tab
	# the chord game only plays one chord at a time
	# each chord is represented as a tab
	# this function is called every time the user hits another chord
	def play_tab_chord_practice(self):
		global song
		global startedATab
		tab = getRandomChord()
		song = chordParser(tab)
		setDoneWithTab(False)
		global t
		t = threading.Thread(target=lightGuitarPractice, args=(song, ''))
		t.daemon = True
		t.start()
		startedATab = True
		
		self.screens[self.challengeIdx].ids.chord_name.text = tab[1]

	# When playing the chord game, the user and the program can both access this variable
	# Lock implemented to ensure neither overwrites the other's changes
	def setPlayingChallenge(self, val):
		global challengeGoingLock
		challengeGoingLock.acquire(True)
		self.challengeGoing = val
		challengeGoingLock.release()

	def getPlayingChallenge(self):
		challengeGoingLock.acquire(True)
		return self.challengeGoing
app = GuitarApp()


# this clock repeatedly checks whether the user has completed a song
# once the user completes a song, it just moves to the scoreboard index
def stopPlayingTabCheck(dt):
	global onScreenTabClock
	global startedATab
	if startedATab and not t.isAlive() and app.index == app.tabLibraryIdx:
		startedATab = False
		app.quit_tab_viewer()
		app.go_screen(app.scoreboardIdx)
		app.screens[app.scoreboardIdx].ids.LastScore.text = app.getLastScore()
		app.screens[app.scoreboardIdx].ids.Score1.text = '1. ' + app.get5Scores()[0]
		app.screens[app.scoreboardIdx].ids.Score2.text = '2. ' + app.get5Scores()[1]
		app.screens[app.scoreboardIdx].ids.Score3.text = '3. ' + app.get5Scores()[2]
		app.screens[app.scoreboardIdx].ids.Score4.text = '4. ' + app.get5Scores()[3]
		app.screens[app.scoreboardIdx].ids.Score5.text = '5. ' + app.get5Scores()[4]
Clock.schedule_interval(stopPlayingTabCheck, .1)

# This is the template for each "screen" in our application
class GuitarScreen(Screen):
	fullscreen = BooleanProperty(False)

	# This function adds the widget to the window, we need this to display the pages
	def add_widget(self, *args):
		if 'content' in self.ids:
			return self.ids.content.add_widget(*args)
		return super(GuitarScreen, self).add_widget(*args)
		
	def dismiss_popup(self):
		self._popup.dismiss()

	# displays the file browser
	def show_load_tab_screen(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	# check if txt file is valid, if so then load the txt file as a tab 
	def load(self, path, filename):
		name = os.path.split(os.path.join(path, filename[0]))[-1]
		# will not load if tab is too long!
		# this is just so tab displays correctly
		if(cleanTab(os.path.join(path, filename[0]), os.path.abspath(os.path.join('.','data/tabs/' + name)))):
			content = Button(text='Success')
		else:
			content = Button(text='Tab too long!')
		
		popup = Popup(title='Result', content=content,  size_hint=(None, None), size=(200, 200), auto_dismiss=False)		
		content.bind(on_press=popup.dismiss)
		popup.open()
		self.dismiss_popup()

# This is the function that listens to the dynamic buttons
# When a button is pressed this function is called with the 
# button returned as an argument.
# With the button returned, we can access its members.
# The id member has the path+file name.
# The text member has just the file name without the .txt
def play_tab(tab, *args):
	global song
	global startedATab
	fn = tab.text + '.txt'
	song = parser(fn)
	setDoneWithTab(False)
	global t
	t = threading.Thread(target=lightGuitar, args=(song, tab.text))
	t.daemon = True
	t.start()
	startedATab = True
	app.currentlyPlayingTab = tab.text


# this is a clock that runs every tenth of a second once the chord practice game is selected
# this function checks if it is time to move onto the next chord in the challenge
def updateChordPractice(dt):
	global practiceChordClock
	global startedATab
	global challengeGoingLock
	stillGoing = app.getPlayingChallenge()
	challengeGoingLock.release()
	if stillGoing and startedATab and not t.isAlive() and app.index == app.challengeIdx:
		startedATab = False
		#update text on screen
		#update score
		app.play_tab_chord_practice()
Clock.schedule_interval(updateChordPractice, .1)

	
########################TUNER######################################	
#! /usr/bin/env python
NOTE_MIN = 40       # E2
NOTE_MAX = 64       # E4
FSAMP = 22050       # Sampling frequency in Hz
FRAME_SIZE = 2048   # samples per frame
FRAMES_PER_FFT = 16  # FFT takes average across how many frames?

######################################################################
# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (sof
# resolution increases); however, it will incur more delay to process
# new sounds.

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT

######################################################################
# For printing out notes
NOTE_NAMES = 'E F F# G G# A A# B C C# D D#'.split()


######################################################################
# These three functions are based upon this very useful webpage:
# https://newt.phys.unsw.edu.au/jw/notes.html

def freq_to_number(f): return 64 + 12 * np.log2(f / 329.63)


def number_to_freq(n): return 329.63 * 2.0**((n - 64) / 12.0)


def note_name(n):
    return NOTE_NAMES[n % NOTE_MIN % len(NOTE_NAMES)] + str(int(n / 12 - 1))

	
def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP


def set_Done_Tuning(state):
	global Done_Tuning
	Done_Tuning = state

	
def tune():

	imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
	imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))

	# Allocate space to run an FFT.
	buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
	num_frames = 0

	# Initialize audio
	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
									channels=1,
									rate=FSAMP,
									input=True,
									frames_per_buffer=FRAME_SIZE)

	stream.start_stream()

	# Create Hanning window function
	window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))

	global Done_Tuning
	
	# As long as we are getting data:
	while stream.is_active() and not Done_Tuning:

		# Shift the buffer down and new data in
		buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
		buf[-FRAME_SIZE:] = np.frombuffer(stream.read(FRAME_SIZE), np.int16)

		# Run the FFT on the windowed buffer
		fft = np.fft.rfft(buf * window)

		# Get frequency of maximum response in range
		freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

		# Get note number and nearest note
		n = freq_to_number(freq)
		n0 = int(round(n))

		# Console output once we have a full buffer
		num_frames += 1

		if num_frames >= FRAMES_PER_FFT:
			app.update_tuner(note_name(n0),n - n0)
	stream.close()

# Run the application
if __name__ == '__main__':
	app.run()
	cl()