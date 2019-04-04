from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder

# Based on code from https://github.com/kivy/kivy/wiki/Scrollable-Label

with open('testing.txt', 'r') as file:
    data = file.read()
long_text = data
Builder.load_string('''
<ScrollableLabel>:
    Label:
        halign: 'left'
        valign: 'middle'
        font_size: 70
        text: root.text
''')


class ScrollableLabel(ScrollView):
    text = StringProperty('')
    

class ScrollApp(App):
    def build(self):
        return ScrollableLabel(text=long_text)

if __name__ == "__main__":
    ScrollApp().run()
