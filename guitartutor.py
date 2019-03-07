'''
This is a prototype of our guitar tutoring app.

The app is implemented in Kivy and python 3.

Current Contributions: Gerardo Mares II

Gerardo Mares II Notes:

'''

import random
import time

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
# Use this for making buttons dynamically
from kivy.uix.button import Button

from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup

import os, sys
a = os.path.abspath(os.path.join('.','Arduino'))
sys.path.append(a)
b = os.path.abspath(os.path.join('.', 'Parsing'))
sys.path.append(b)
c = os.path.abspath(os.path.join('.','Note Recognition, etc'))
sys.path.append(c)

from Lights import *
from Parser import *
from Chords import *

# This is the function that listens to the dynamic buttons
# When a button is pressed this function is called with the 
# button returned as an argument.
# With the button returned, we can access its members.
# The id member has the path+file name.
# The text member has just the file name without the .txt
def play_tab(tab, *args):
	pass
	#print(tab.id)

# This will be the class representing each screen
# There is currently no logic in each screen


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class GuitarScreen(Screen):
	fullscreen = BooleanProperty(False)

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

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		with open(os.path.join(path, filename[0])) as stream:
			self.text_input.text = stream.read()
		self.dismiss_popup()

	def save(self, path, filename):
		with open(os.path.join(path, filename), 'w') as stream:
			stream.write(self.text_input.text)
		self.dismiss_popup()
	

class GuitarApp(App):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	text_input = ObjectProperty(None)
	
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
			"TabLibrary", "AddTab", "Challenge"]
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
	
	# Dynamically make buttons for all tab files in the tabs folder
	def load_tabs(self, tab_page):
		#tab_page.bind(minimum_height=tab_page.setter('height'))
		# delete all previous buttons!
		# this way we don't duplicate buttons
		#tab_page.clear_widgets()
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
			button.bind(on_release= play_tab)
			# Add button!
			tab_page.add_widget(button)

if __name__ == '__main__':
	GuitarApp().run()
