
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior

Window.size = (360, 640)
#Window.clearcolor = (1, 1, 1, 1)

class MainGrid(GridLayout):
    pass


class MainApp(App):
    def build(self):
        return MainGrid()

if __name__ == "__main__":
    MainApp().run()