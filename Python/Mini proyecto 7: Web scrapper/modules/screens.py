import csv
import datetime
import os
import re
import time

from kivy.core.text import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from item_result import Item
from result_found import ResultFound


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []

        layout = BoxLayout(orientation='vertical')

        self.text_input = TextInput()
        add_button = Button(text='+', on_press=self.add_item)
        add_layout = BoxLayout(orientation='horizontal')
        add_layout.add_widget(self.text_input)
        add_layout.add_widget(add_button)
        layout.add_widget(add_layout)

        self.items_label = Label(text='No se han agregado elementos')
        layout.add_widget(self.items_label)

        send_button = Button(text='Enviar', background_color=(0, 1, 0, 1))
        send_button.bind(on_press=self.open_search_screen)
        layout.add_widget(send_button)

        self.add_widget(layout)

    def add_item(self, instance):
        item = self.text_input.text.strip()
        if item:
            self.items.append(item)
            self.text_input.text = ''
            self.update_items_label()
        else:
            self.show_error_message("El elemento introducido está vacío!")

    def update_items_label(self):
        if self.items:
            self.items_label.text = '\n'.join(self.items)
        else:
            self.items_label.text = 'No se han agregado elementos'

    def open_search_screen(self, instance):
        search_screen = SearchScreen(items=self.items)
        self.manager.transition.direction = 'left'
        self.manager.switch_to(search_screen)

    @staticmethod
    def show_error_message(message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(600, 600))
        popup.open()


class SearchScreen(Screen):
    def __init__(self, items, **kwargs):
        super().__init__(**kwargs)
        self.items = items

        layout = BoxLayout(orientation='vertical')

        results_label = Label(text='Resultados:')
        layout.add_widget(results_label)

        # Mostrar los resultados de los items
        for item in self.items:
            result_label = Label(text=item)
            layout.add_widget(result_label)

        back_button = Button(text='Volver', background_color=(1, 0, 0, 1))
        back_button.bind(on_press=self.open_home_screen)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def open_home_screen(self):
        home_screen = HomeScreen()
        self.manager.transition.direction = 'right'
        self.manager.switch_to(home_screen)

    def on_enter(self, *args):
        self.search_in_sites()

    def handle_heb_call(self, driver, url: str):
        driver.get(url)

        items_array = []

        for itemToFind in self.items:
            time.sleep(2)

            find_box = driver.find_element(By.CSS_SELECTOR, '[placeholder="Buscar productos"]')
            find_box.send_keys(itemToFind.lower())
            find_box.send_keys(Keys.RETURN)

            wait = WebDriverWait(driver, 10)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.vtex-search-result-3-x-gallery')))

            grid_view = driver.find_element(
                By.CSS_SELECTOR, '.vtex-search-result-3-x-gallery')
            rows = grid_view.find_elements(By.TAG_NAME, 'div')
            item = Item(itemToFind)
            for row in rows:
                if row.text != '':
                    add_word = self.handle_result(row.text, itemToFind)
                    if add_word:
                        result = ResultFound(row.text, 'HEB')
                        item.results.append(result)
                    continue

            items_array.append(item)
            driver.back()
            time.sleep(2)
            continue

        driver.close()
        return items_array

    @staticmethod
    def handle_result(result, item):
        lowercase_result = result.lower()
        lowercase_item = item.lower()

        words = lowercase_item.split()
        num_words = len(words)

        if num_words == 1:
            return lowercase_item in lowercase_result and '$' in result
        elif num_words == 2:
            word1, word2 = words
            return (word1 in lowercase_result or word2 in lowercase_result) and '$' in result

        return False

    def search_in_sites(self):
        urls = ['https://www.heb.com.mx/']
        driver = webdriver.Chrome()
        result = self.handle_heb_call(driver, urls[0])
        title = 'hbe-results-{}:{}.csv'.format(
            datetime.datetime.now().hour,
            datetime.datetime.now().minute)
        self.write_results(title, result)

    @staticmethod
    def get_result_description(result):
        title_pattern = r'^(.*?)\$'
        title_match = re.search(title_pattern, result, re.MULTILINE | re.DOTALL)
        return title_match.group(1).strip()

    @staticmethod
    def get_result_price(result):
        price_pattern = r'\$(\d+(\.\d{2})?)'
        price_match = re.search(price_pattern, result)
        return price_match.group(1)

    def write_results(self, file_name, results):
        if not os.path.exists('./results'):
            os.makedirs('./results')

        path = os.path.join('./results', file_name)

        with open(path, 'w', newline='') as file:
            writter = csv.writer(file)
            writter.writerow(['Nombre producto', 'Resultado', 'Precio', 'Tienda'])

            for item in results:
                name = item.name
                for item_result in item.results:
                    site = item_result.site
                    description = self.get_result_description(item_result.result)
                    price = self.get_result_price(item_result.result)
                    writter.writerow([name, description, price, site])
        print(f'File saved: {file_name}')
