from kivy.app import App
from kivy.uix.gridlayout import GridLayout

app = App()


class Container(GridLayout):
    def change_text(self):
        self.label_widget.text = self.krakozjabra.text.upper()


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MyApp().run()
