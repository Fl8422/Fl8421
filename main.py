import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
import requests
import json

# Установка черного фона
Window.clearcolor = (0, 0, 0, 1)

KV = """
<ParserPanel>:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    Label:
        text: "Parser Panel"
        font_size: 24
        color: 0, 0, 1, 1  # Синий цвет
        bold: True
        size_hint_y: None
        height: 40

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 40
        spacing: 10

        TextInput:
            id: search_input
            hint_text: "Введите поисковый запрос"
            background_color: 1, 1, 1, 1
            multiline: False

        Button:
            text: "Поиск"
            background_color: 0, 0, 0, 1
            color: 1, 1, 1, 1
            on_press: root.perform_search()

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 40
        spacing: 10
        padding: (0, 10, 0, 10)

        Spinner:
            id: search_type
            text: "Стандартный поиск"
            values: [
                "Стандартный поиск",
                "Подробный поиск",
                "Поиск по времени",
                "Поиск по сайту"
            ]
            size_hint: (0.5, 1)
            on_text: root.change_search_type(self.text)

    ScrollView:
        id: results_scroll
        do_scroll_x: False

        BoxLayout:
            id: results_box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: 10
            spacing: 10

    Label:
        id: status_label
        text: ""
        color: 1, 1, 1, 1
        size_hint_y: None
        height: 30
"""

class ParserPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(ParserPanel, self).__init__(**kwargs)
        self.api_key = "YOUR_GOOGLE_API_KEY"
        self.cse_id = "YOUR_CSE_ID"
        self.current_search = "Стандартный поиск"

    def change_search_type(self, search_type):
        self.current_search = search_type
        self.ids.status_label.text = f"Текущий поиск: {search_type}"

    def perform_search(self):
        query = self.ids.search_input.text
        if not query:
            self.ids.status_label.text = "Введите запрос для поиска."
            return

        # Отображение индикатора загрузки
        self.ids.results_box.clear_widgets()
        loading_label = Label(text="Загрузка...", color=(1,1,1,1), size_hint_y=None, height=30)
        self.ids.results_box.add_widget(loading_label)

        # Определение типа поиска
        if self.current_search == "Стандартный поиск":
            final_query = query
        elif self.current_search == "Подробный поиск":
            final_query = f'{query} "подробный"'
        elif self.current_search == "Поиск по времени":
            final_query = f'{query} "последняя неделя"'
        elif self.current_search == "Поиск по сайту":
            final_query = f'{query} site:название_сайта.com'
        else:
            final_query = query

        # Запрос к Google Custom Search API
        url = f"https://www.googleapis.com/customsearch/v1?q={final_query}&key={self.api_key}&cx={self.cse_id}"
        response = requests.get(url)

        # Обработка ответа
        self.ids.results_box.clear_widgets()
        if response.status_code == 200:
            results = response.json()
            items = results.get("items", [])
            if not items:
                self.ids.results_box.add_widget(Label(text="Нет результатов.", color=(1,1,1,1), size_hint_y=None, height=30))
                return
            for item in items:
                link = item.get("link", "Нет ссылки")
                self.ids.results_box.add_widget(Button(text=link, size_hint_y=None, height=40, background_color=(0,0,0,1), color=(1,1,1,1)))
        else:
            self.ids.results_box.add_widget(Label(text="Ошибка при поиске.", color=(1,1,1,1), size_hint_y=None, height=30))

class ParserApp(App):
    def build(self):
        Builder.load_string(KV)
        return ParserPanel()

if __name__ == '__main__':
    ParserApp().run()
