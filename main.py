from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

app = App()


class Container(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MyApp().run
