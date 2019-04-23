from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label

with open('testing.txt', 'r') as file:
    data = file.read()

Builder.load_string("""
<ScrollSlider>:
    ScrollView:
        id: scrlvw
        bar_height: 0
        GridLayout:
            id: grid
            size_hint_x:None
            rows:1
            width: self.minimum_width
            scroll_x: slider.value
            on_touch_move: slider.value = self.scroll_x
    Slider:
        size_hint_y: None
        height: root.height*0.2
        id: slider
        min: 0
        max: 1
        orientation: 'horizontal'
        value: scrlvw.scroll_x
        on_value: scrlvw.scroll_x = self.value

""")


class ScrollSlider(BoxLayout):

    def custom_add(self, widget):
        self.ids.grid.add_widget(widget)

class MyApp(App):


    def build(self):
        scrollslider = ScrollSlider()
        for i in range(1, 100):
            scrollslider.custom_add(Label(text=str(data), width=100, size_hint_x=None))
        return scrollslider

if __name__ == '__main__':
    MyApp().run()
