import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen


Window.size = 360, 640
Window.clearcolor = 1,1,1,1

class GridButton(ButtonBehavior, GridLayout):
    pass

class MainWindow(Screen):
    def mycall_back(self):
        print("This button is working")
    pass

class RecipesWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv=Builder.load_file("main.kv")


class MainApp(App):
    title= "Como en Casa"
    def build(self):
        return kv

if __name__ == "__main__":
    MainApp().run() 
