from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from pyparsing import *
import fileinput

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

class TestingW(Widget):
    btn = ObjectProperty(None)
	
    def build(self):
        return

class TestingApp(App):
    def foo(self):
        chords()

    def build(self):
        return TestingW()

if __name__ == '__main__':
    TestingApp().run()