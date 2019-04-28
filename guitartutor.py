'''
This is a prototype of our guitar tutoring app.

The app is implemented in Kivy and python 3.

Current Contributions: Gerardo Mares II

Gerardo Mares II Notes:

'''

import builtins
import random
import time

import threading

# Used to get directory to different 'screens'
import os
from os.path import dirname, join
# Defalut kivy app object, we need this to make kivy work
from kivy.app import App
# Use properties to link variables from the python file to the kivy screens
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
# Use to manage screen switching
from kivy.uix.screenmanager import Screen
# Use builder to run kivy code inside of python
from kivy.lang import Builder
# Glob is a module that finds all the path names matching a specified pattern
import glob
# Use this to get names of tabs and paste them to buttons
import re

import numpy as np
import pyaudio

# Use this for making buttons dynamically
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

import threading
from queue import Queue
import time

import sys
import shutil
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




# scroller for scrolling
#scroll = ScrollView()
# gets a random chord name from a list of all implemented chords
# used for simon says game
def getRandomChord():
	possibleChords = [ac,a7c,amc,am7c,amaj7c,bfc,b7c,bmc,cc,c7c,cmaj7c,dc,d7c,dmc,dm7c,dmaj7c,ec,e7c,emc,em7c,fc,fmaj7c,gc,g7c]
	return random.choice(possibleChords)
		
class OneMoreNoteWidget(Widget):
	oneMoreNoteClock = 0
	def __init__(self, **kwargs):
		super(OneMoreNoteWidget, self).__init__(**kwargs)
		self.oneMoreNoteClock = Clock.schedule_interval(self.update, 1/60.)
	
	def update(self, *args):
		if not t.isAlive() and app.index == app.oneMoreNoteIdx:
			app.go_screen(app.homeScreenIdx)

song = 0

def getFretPressed(frets):
	fretPressed = -1
	try:
		fretPressed = frets.index(True) 
	except:
		return '-'
	return str(fretPressed + 1)

onScreenTabClock = 0

class OnScreenTab(Widget):
	stringEHigh = StringProperty()
	stringB = StringProperty()
	stringG = StringProperty()
	stringD = StringProperty()
	stringA = StringProperty()
	stringE = StringProperty()

	def __init__(self, **kwargs):
		global onScreenTabClock
		super(OnScreenTab, self).__init__(**kwargs)
		onScreenTabClock = Clock.schedule_interval(self.update, 1/60.)
	
	def update(self, *args):
		global song
		(measure, note, fret) = getSongPosition()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class GuitarApp(App):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	text_input = ObjectProperty(None)
	currentlyPlayingTab = StringProperty()
	
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

	# demo simon says
	# still need to make it listen


	def challenge(self):
		chordsSoFar = []

		#while (True):
		chordsSoFar.append(getRandomChord())
		for c in chordsSoFar:
			#self.displayChord(c)
			self.screens[self.challengeIdx].ids.chord_name.text = c[1]
			time.sleep(1)
	
	def build(self):
		# Title of window
		self.title = 'Guitar Tutor'
		# Initialize the list of screen that app has
		self.screens = {}
		# Add screens to the list
		self.available_screens = ["HomeScreen", "ChordLibrary",
			"TabLibrary", "AddTab", "Challenge", "Tuner", "PlayingTab", 
			"OneMoreNote", "Scoreboard"]
		self.homeScreenIdx = 0
		self.chordLibraryIdx = 1
		self.tabLibraryIdx = 2
		self.addTabIdx = 3
		self.challengeIdx = 4
		self.tunerIdx = 5
		self.playingTabIdx = 6
		self.oneMoreNoteIdx = 7
		self.scoreboardIdx = 8
		# Remember names of screens, used for loading files
		self.screen_names = self.available_screens
		# Get current directory
		curdir = dirname(__file__)
		# Re-fill available screens with the path to each screen
		self.available_screens = [join(curdir, 'data', 'screens',
			'{}.kv'.format(fn).lower()) for fn in self.available_screens]
		# Initialize first screen (index 0)
		self.go_screen(self.homeScreenIdx)

	#Testing with showing source code
	def toggle_source_code(self,*args):
		height = self.root.height * .5
		
		Animation(height=height, d=.3, t='out_quart').start(
			self.root.ids.sv)
		
		self.update_sourcecode(args[0])

	def clear(self):
		cl()

	def quit_source_code(self, *args):
		Animation(height=0, d=.3, t='out_quart').start(self.root.ids.sv)
		
	def read_sourcecode(self, *args):
		fn = self.available_screens[self.index]
		curdir = dirname(__file__)
		fn = args[0].text
		fn = join(curdir, 'data', 'tabs', '{}.txt'.format(fn))

		with open(fn) as fd:
			# get length of a single line to get horizontal scroll
			line = fd.readline()
			# 9.1 is a magic number used to get the right width for horizontal scrolling
			# Max tab length is 1800
			self.root.ids.sourcecode.width = 9.1 * len(line)
			fd.seek(0)
			
			# return actual tab to display
			return fd.read()
	
	def update_sourcecode(self, *args):
		self.root.ids.sourcecode.text = self.read_sourcecode(args[0])
		self.root.ids.sv.scroll_y = 1
		self.root.ids.sv.scroll_x = 0
		
		# animate scroll
		scroll = self.root.ids.sv
		move = Animation(scroll_x=1, duration=200.0)
		move.start(scroll)
	
	def go_screen(self, idx):
		#cl()
		if(t.isAlive() and self.index != self.oneMoreNoteIdx and self.index != self.tabLibraryIdx):
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
		
	def do_tuning(self):
		tuner_page = self.screens[5].layout
		tuner_page.clear_widgets()
		
		button = Label()
		button.text = 'Starting Tuner...'
		button.font_size = '20dp'
		button.bind(on_release = app.start_tuner)
		tuner_page.add_widget(button)
		
	def update_tuner(self, note_name, cents):
		tuner_page = self.screens[5].layout
		tuner_page.clear_widgets()
		
		label = Label()
		title = Label()
		
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
		label.text = note_name
		label.font_size = '100dp'
		
		
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
			button.bind(on_release = self.toggle_source_code)
			# Add button!
			tab_page.add_widget(button)
	
	def stopTab(self):
		if (not getDoneWithTab()):
			setDoneWithTab(True)
			cl()
			global startedATab
			startedATab = False
			#app.toggle_source_code()
			app.go_screen(self.oneMoreNoteIdx)

	def stopChord(self):
		if (not getDoneWithTab()):
			global startedATab
			startedATab = False
			setDoneWithTab(True)
			cl()
			#app.toggle_source_code()
			app.go_screen(self.oneMoreNoteIdx)

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

	def getLastScore(self):
		# file = open("Scores/" + self.currentlyPlayingTab + ".txt")
		# scores = []
		# for line in file:
		# 	scores.append(line[:-1])
		# if len(scores) < 1:
		# 	return ''
		# return scores[-1]
		return getTheLastScore()

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
		#app.currentlyPlayingTab = ''
		#app.go_screen(app.playingTabIdx)

app = GuitarApp()

startedATab = False

def stopPlayingTabCheck(dt):
	global onScreenTabClock
	global startedATab
	if startedATab and not t.isAlive() and app.index == app.tabLibraryIdx:
		startedATab = False
		app.quit_source_code()
		app.go_screen(app.scoreboardIdx)
		app.screens[app.scoreboardIdx].ids.LastScore.text = app.getLastScore()
		app.screens[app.scoreboardIdx].ids.Score1.text = '1. ' + app.get5Scores()[0]
		app.screens[app.scoreboardIdx].ids.Score2.text = '2. ' + app.get5Scores()[1]
		app.screens[app.scoreboardIdx].ids.Score3.text = '3. ' + app.get5Scores()[2]
		app.screens[app.scoreboardIdx].ids.Score4.text = '4. ' + app.get5Scores()[3]
		app.screens[app.scoreboardIdx].ids.Score5.text = '5. ' + app.get5Scores()[4]

Clock.schedule_interval(stopPlayingTabCheck, .1)

class GuitarScreen(Screen):
	fullscreen = BooleanProperty(False)
	print(getRandomChord())

	# This function adds the widget to the window, we need this to display the pages
	def add_widget(self, *args):
		if 'content' in self.ids:
			return self.ids.content.add_widget(*args)
		return super(GuitarScreen, self).add_widget(*args)
		
	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

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
	
	def update(self):
		global t
		print('pp')
		if app.current_title() == 'PlayingTab':
			if not t.isAlive():
				app.go_screen(app.addTabIdx)

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
	print(len(song))
	setDoneWithTab(False)
	global t
	t = threading.Thread(target=lightGuitar, args=(song, tab.text))
	t.daemon = True
	t.start()
	startedATab = True
	app.currentlyPlayingTab = tab.text
	#app.go_screen(app.playingTabIdx)



practiceChordClock = 0

def updateChordPractice(dt):
	global practiceChordClock
	global startedATab
	if startedATab and not t.isAlive() and app.index == app.challengeIdx:
		startedATab = False
		#update text on screen
		#update score
		app.play_tab_chord_practice()

Clock.schedule_interval(updateChordPractice, .1)

	
########################TUNER######################################	
'''
	Credits: 
		GitHub user handles: mzucker, michniewicz
		URL: https://github.com/michniewicz/python-tuner/graphs/contributors
		
'''

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

######################################################################
# Ok, ready to go now.

# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()


def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP


Done_Tuning = False

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

	# Print initial text
	#print('sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')
	#print()

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
			#print('number {:7.2f} freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(n,
			#																		freq, note_name(n0), n - n0))
	stream.close()

if __name__ == '__main__':
	# try:
	app.run()
	# except Exception as e:
		# print(e)
		# cl()
	cl()