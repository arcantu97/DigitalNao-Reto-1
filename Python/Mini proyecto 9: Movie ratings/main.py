import http.client
import json

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class ListItem(BoxLayout):
    def __init__(self, title, year, image_url, rating, **kwargs):
        super(ListItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '120dp'

        image = AsyncImage(source=image_url, size_hint=(None, 1), width='100dp')
        self.add_widget(image)

        title_label = Label(text=title, size_hint=(None, 1), width='200dp')
        self.add_widget(title_label)

        year_label = Label(text=year, size_hint=(None, 1), width='300dp')
        self.add_widget(year_label)

        rating_label = Label(text=str(rating), size_hint=(None, 1), width='200dp')
        self.add_widget(rating_label)


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        scroll_view = ScrollView()
        layout.add_widget(scroll_view)

        list_layout = BoxLayout(orientation='vertical', spacing='20dp', size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        scroll_view.add_widget(list_layout)

        Clock.schedule_once(lambda dt: self.consume_api(list_layout), 0.1)

        return layout

    @staticmethod
    def consume_api(list_layout):
        api = http.client.HTTPSConnection("moviesdatabase.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': "",
            'X-RapidAPI-Host': "moviesdatabase.p.rapidapi.com"
        }

        api.request('GET', '/titles?limit=40&endYear=2022', headers=headers)

        res = api.getresponse()
        data = res.read()

        json_data = json.loads(data.decode('utf-8'))

        items = json_data.get('results', [])

        list_items = []

        for item in items:
            api.request('GET', '/titles/{}/ratings'.format(item['id']), headers=headers)
            res = api.getresponse()
            data = res.read()
            json_data = json.loads(data.decode('utf-8'))
            rating = json_data.get('results')
            default_image_url = "https://cdn.vectorstock.com/i/preview-1x/32/45/no-image-symbol-missing-available" \
                                "-icon-gallery-vector-45703245.jpg"
            list_item = ListItem(
                title=item["titleText"]["text"],
                year=str(item["releaseYear"]["year"]),
                image_url=item["primaryImage"]["url"] if item["primaryImage"] is not None else default_image_url,
                rating=str(rating['averageRating']) if rating is not None and 'averageRating' in rating else '0'

            )

            list_items.append(list_item)

        for item in list_items:
            list_layout.add_widget(item)


if __name__ == '__main__':
    MyApp().run()
