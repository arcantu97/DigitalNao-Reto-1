from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class HangmanGame(App):
    def __init__(self, **kwargs):
        super(HangmanGame, self).__init__(**kwargs)
        self.word = "DIGITALNAO"
        self.guesses = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.word_label = Label(text=self.display_word())
        layout.add_widget(self.word_label)

        self.guess_label = Label(text="Intentos restantes: {}".format(self.attempts_left))
        layout.add_widget(self.guess_label)

        buttons_layout = BoxLayout()
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            button = Button(text=letter, on_press=self.make_guess)
            buttons_layout.add_widget(button)

        layout.add_widget(buttons_layout)

        return layout

    def make_guess(self, instance):
        letter = instance.text
        self.guesses.add(letter)

        if letter not in self.word:
            if self.attempts_left > 0:
                self.attempts_left -= 1

        self.word_label.text = self.display_word()
        self.guess_label.text = "Intentos restantes: {}".format(self.attempts_left)

        self.end_game()

    def display_word(self):
        return " ".join([letter if letter in self.guesses else "_" for letter in self.word])

    def end_game(self):
        if self.attempts_left <= 0:
            self.word_label.text = "Perdiste. La palabra era: {}".format(self.word)
            self.disable_buttons()
        elif "_" not in self.display_word():
            self.word_label.text = "¡Ganaste!"
            self.disable_buttons()

    def disable_buttons(self):
        for button in self.root.children[0].children[2].children:
            button.disabled = True


if __name__ == '__main__':
    HangmanGame().run()
