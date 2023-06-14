from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class NumbersLayout(GridLayout):
    def __init__(self, **kwargs):
        super(NumbersLayout, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 10
        self.padding = [10, 10, 10, 10]

        numbers_label = Label(text='', font_size=50, size_hint=(1, None), height=50)
        self.add_widget(Label())
        self.add_widget(numbers_label)
        self.add_widget(Label(height=50))

        numbers = list(range(10))
        numbers.extend(['*', '0', '#'])
        for number in numbers:
            button = Button(text=str(number))
            button.bind(on_release=self.update_numbers)
            self.add_widget(button)

        delete_button = Button(text='X')
        delete_button.bind(on_release=self.delete_last_digit)
        self.add_widget(delete_button)

        self.numbers_label = numbers_label

    def update_numbers(self, button):
        self.numbers_label.text += button.text

    def delete_last_digit(self, button):
        numbers = self.numbers_label.text
        if numbers:
            self.numbers_label.text = numbers[:-1]


class PhoneApp(App):
    def build(self):
        return NumbersLayout()


if __name__ == '__main__':
    PhoneApp().run()
