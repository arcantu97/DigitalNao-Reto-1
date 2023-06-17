from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle


class ColorSelector(Button):
    def __init__(self, color, paint_widget, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.paint_widget = paint_widget
        self.background_color = color

    def on_release(self):
        self.paint_widget.current_color = self.color


class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_color = (0, 0, 0)
        self.lines = []

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.current_color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=2)
            self.lines.append(touch.ud['line'])

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    def clear_last_line(self):
        if self.lines:
            last_line = self.lines.pop()
            self.canvas.remove(last_line)

    def clear_canvas(self):
        self.canvas.clear()
        self.lines = []


class PaintApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        paint_widget = PaintWidget()
        layout.add_widget(paint_widget)

        color_selector_layout = BoxLayout(size_hint=(1, None), height=50)
        colors = [
            (0, 0, 0),  # Negro
            (0.5, 0.5, 0.5),  # Gris
            (0, 0, 1),  # Azul
            (0, 1, 0),  # Verde
            (1, 1, 0),  # Amarillo
            (1, 0, 0)  # Rojo
        ]
        for color in colors:
            color_selector = ColorSelector(color=color, paint_widget=paint_widget, size_hint_x=1)
            color_selector_layout.add_widget(color_selector)

        layout.add_widget(color_selector_layout)

        clear_last_button = Button(text='Borrar último trazo', size_hint=(1, None), height=50)
        clear_last_button.bind(on_release=lambda x: paint_widget.clear_last_line())
        layout.add_widget(clear_last_button)

        clear_button = Button(text='Borrar todo', size_hint=(1, None), height=50)
        clear_button.bind(on_release=lambda x: paint_widget.clear_canvas())
        layout.add_widget(clear_button)

        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanco
            layout.rect = Rectangle(pos=layout.pos, size=layout.size)

        layout.bind(pos=self.update_rect, size=self.update_rect)

        return layout

    @staticmethod
    def update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


if __name__ == '__main__':
    PaintApp().run()
