from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from screens import HomeScreen


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = ScreenManager(transition=SlideTransition())

    def build(self):
        self.manager.add_widget(HomeScreen(name='home'))
        return self.manager


if __name__ == '__main__':
    MainApp().run()
