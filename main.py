from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from search_engine import perform_search

class ParserPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 20
        self.spacing = 10

        # Заголовок
        self.add_widget(Label(
            text="Parser Panel",
            font_size="24sp",
            bold=True,
            color=(0, 0, 1, 1),  # Синий цвет
            size_hint=(1, 0.1)
        ))

        # Поисковая строка
        self.search_input = TextInput(
            hint_text="Введите запрос...",
            size_hint=(1, 0.1),
            multiline=False,
            background_color=(0, 0, 0, 1),  # Черный фон
            foreground_color=(1, 1, 1, 1),  # Белый текст
        )
        self.add_widget(self.search_input)

        # Выпадающее меню
        self.search_type_spinner = Spinner(
            text="Стандартный поиск",
            values=("Стандартный поиск", "Подробный поиск", "Поиск по времени", "Поиск по сайту"),
            size_hint=(1, 0.1),
        )
        self.add_widget(self.search_type_spinner)

        # Кнопка "Поиск"
        self.search_button = Button(
            text="Поиск",
            size_hint=(1, 0.1),
            background_color=(0, 0, 1, 1),  # Синий цвет
            on_press=self.start_search
        )
        self.add_widget(self.search_button)

        # Окно для результатов
        self.result_view = ScrollView(size_hint=(1, 1))
        self.result_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        self.result_view.add_widget(self.result_layout)
        self.add_widget(self.result_view)

    def start_search(self, instance):
        query = self.search_input.text
        search_type = self.search_type_spinner.text

        if query.strip() == "":
            self.show_message("Введите запрос!")
            return

        # Очистка результатов
        self.result_layout.clear_widgets()
        self.show_message("Идет поиск...")

        # Выполнение поиска
        Clock.schedule_once(lambda dt: self.perform_search(query, search_type), 1)

    def perform_search(self, query, search_type):
        results = perform_search(query, search_type)
        self.result_layout.clear_widgets()

        if not results:
            self.show_message("Ничего не найдено.")
            return

        for link in results:
            self.result_layout.add_widget(Label(text=link, size_hint_y=None, height=40))

    def show_message(self, message):
        self.result_layout.clear_widgets()
        self.result_layout.add_widget(Label(text=message, size_hint_y=None, height=40))


class ParserPanelApp(App):
    def build(self):
        return ParserPanel()


if __name__ == "__main__":
    ParserPanelApp().run()
