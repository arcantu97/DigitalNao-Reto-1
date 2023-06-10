from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from exceptions import exceptions
from modules import converter


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        self.numbers_to_words = converter.NumberToWords()
        self.result_label = None

    def build(self):
        layout = BoxLayout(orientation='vertical')

        label = Label(text="Ingresa un número en el campo blanco")
        layout.add_widget(label)

        input_text = TextInput(
            multiline=False,
            font_size=124,
            halign="center")
        layout.add_widget(input_text)

        button = Button(text="Convertir", on_release=self.handle_conversion)
        layout.add_widget(button)

        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        return layout

    def handle_conversion(self, instance):
        try:
            number = int(self.root.children[2].text)
            try:
                result = self.numbers_to_words.convert(number)
                self.result_label.text = result
            except exceptions.LargerNumberException as e:
                self.result_label.text = str(e)
        except ValueError:
            self.result_label.text = "El valor ingresado no es un número válido!"
            return
        if number > 199:
            self.result_label.text = "Introduce un valor menor a 199!"


if __name__ == '__main__':
    MainApp().run()
