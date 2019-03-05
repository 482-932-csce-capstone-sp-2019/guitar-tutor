'''
This is a prototype of our guitar tutoring app.

The app is implemented in Kivy and python 3. 

Current Contributions: Gerardo Mares II

Gerardo Mares II Notes:
	
'''

import random
import time

# Used to get directory to different 'screens'
from os.path import dirname, join
# Defalut kivy app object, we need this to make kivy work
from kivy.app import App
# Use properties to link variables from the python file to the kivy screens
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
# Use to manage screen switching
from kivy.uix.screenmanager import Screen
# Use builder to run kivy code inside of python
from kivy.lang import Builder

import os, sys
a = os.path.abspath(os.path.join('.','../Arduino'))
sys.path.append(a)
b = os.path.abspath(os.path.join('.', '../Parsing'))
sys.path.append(b)
c = os.path.abspath(os.path.join('.','../Note Recognition, etc'))
sys.path.append(c)

from Lights import *
from Parser import *
from Chords import *

# This will be the class representing each screen
# There is currently no logic in each screen
class GuitarScreen(Screen):
	fullscreen = BooleanProperty(False)
	
	# This function adds the widget to the window, we need this to display the pages
	def add_widget(self, *args):
		if 'content' in self.ids:
			return self.ids.content.add_widget(*args)
		return super(GuitarScreen, self).add_widget(*args)
	
class GuitarApp(App):
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

	def getRandomChord(self):
		possibleChords = ["a","a7","am","am7","amaj7","bf","b7","bm","c","c7","cmaj7","d","dm","d7","dm7","dmaj7","e","e7","em","em7","f","fmaj7","g","g7"]
		return random.choice(possibleChords)


	def playSimonSays(self):
		chordsSoFar = []

		while (True):
			chordsSoFar.append(self.getRandomChord())
			for c in chordsSoFar:
				self.displayChord(c)
				time.sleep(1)


	
	def build(self):
		# Title of window
		self.title = 'Guitar Tutor'
		# Initialize the list of screen that app has 
		self.screens = {}
		# Add screens to the list
		self.available_screens = ["HomeScreen", "ChordLibrary",
			"TabLibrary","AddTab","Challenge"]
		# Remember names of screens, used for loading files
		self.screen_names = self.available_screens
		# Get current directory
		curdir = dirname(__file__)
		# Re-fill available screens with the path to each screen
		self.available_screens = [join(curdir, 'data', 'screens',
			'{}.kv'.format(fn).lower()) for fn in self.available_screens]
		# Initialize first screen (index 0)
		self.go_screen(0)
	
	def go_screen(self, idx):
		cl()
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
		
if __name__ == '__main__':
	GuitarApp().run()