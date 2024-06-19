import json
import os

from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (480, 853)


class NoteScreen(Screen):
    note_name = StringProperty("")

    def save_note(self):
        note_name = self.ids.name_of_decision.text.strip()
        if note_name:
            note_data = {
                "name_of_decision": self.ids.name_of_decision.text,
                "add_pulse": self.ids.add_pulse.text,
                "add_minus": self.ids.add_minus.text,
                "answer_1": self.ids.answer_1.text,
                "answer_2": self.ids.answer_2.text,
                "answer_3": self.ids.answer_3.text,
                "answer_4": self.ids.answer_4.text
            }
            note_filename = f"{note_name}.json"
            with open(note_filename, 'w', encoding='utf-8') as file:
                json.dump(note_data, file, ensure_ascii=False)

            self.manager.get_screen('main').add_note_button(note_name)
            self.manager.current = 'main'

    def load_note_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            note_data = json.load(file)
            self.ids.name_of_decision.text = note_data['name_of_decision']
            self.ids.add_pulse.text = note_data['add_pulse']
            self.ids.add_minus.text = note_data['add_minus']
            self.ids.answer_1.text = note_data['answer_1']
            self.ids.answer_2.text = note_data['answer_2']
            self.ids.answer_3.text = note_data['answer_3']
            self.ids.answer_4.text = note_data['answer_4']


class MainScreen(Screen):
    def on_pre_enter(self):
        self.ids.notes_layout.clear_widgets()
        for filename in os.listdir('.'):
            if filename.endswith('.json'):
                note_name = filename[:-5]
                self.add_note_button(note_name)

    def add_note_button(self, title):
        btn = Button(text=title, size_hint_y=None, height=40)
        btn.bind(on_release=self.open_note)
        del_btn = Button(text='X', size_hint_y=None, height=40, width=40, size_hint_x=None)
        del_btn.bind(on_release=lambda instance: self.delete_note_button(title))
        container = BoxLayout(size_hint_y=None, height=40)
        container.add_widget(btn)
        container.add_widget(del_btn)
        self.ids.notes_layout.add_widget(container)

    def open_note(self, instance):
        note_filename = f"{instance.text}.json"
        note_screen = self.manager.get_screen('note')
        note_screen.note_name = instance.text
        note_screen.load_note_data(note_filename)
        self.manager.current = 'note'

    def delete_note_button(self, note_name):
        note_filename = f"{note_name}.json"
        if os.path.exists(note_filename):
            os.remove(note_filename)
        self.on_pre_enter()


class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(NoteScreen(name='note'))
        return sm


if __name__ == '__main__':
    MyApp().run()
