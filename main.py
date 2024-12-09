from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
import threading
from libs.parser import perform_search

class ParserPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Заголовок
        self.add_widget(Label(text='Parser Panel', font_size='24sp', color=(0, 0, 1, 1), size_hint=(1, 0.1)))

        # Поле для ввода запроса
        self.search_input = TextInput(hint_text='Введите запрос...', size_hint=(1, 0.1), multiline=False)
        self.add_widget(self.search_input)

        # Спиннер для выбора типа поиска
        self.search_type_spinner = Spinner(
            text='Стандартный поиск',
            values=('Стандартный поиск', 'Подробный поиск', 'Поиск по времени', 'Поиск по сайту'),
            size_hint=(1, 0.1),
            background_color=(0, 0, 1, 1)
        )
        self.add_widget(self.search_type_spinner)

        # Кнопка поиска
        self.search_button = Button(text='Поиск', size_hint=(1, 0.1), background_color=(0, 0, 1, 1))
        self.search_button.bind(on_press=self.on_search)
        self.add_widget(self.search_button)

        # Окно для отображения результатов
        self.results_box = ScrollView(size_hint=(1, 0.7), do_scroll_y=True)
        self.results_label = Label(text='Результаты будут здесь.', size_hint_y=None, markup=True)
        self.results_label.bind(size=self.update_height)
        self.results_box.add_widget(self.results_label)
        self.add_widget(self.results_box)

    def on_search(self, instance):
        query = self.search_input.text
        search_type = self.search_type_spinner.text

        if not query.strip():
            self.results_label.text = 'Введите запрос.'
            return

        self.results_label.text = '[b]Идет поиск...[/b]'
        threading.Thread(target=self.perform_search, args=(query, search_type)).start()

    def perform_search(self, query, search_type):
        results = perform_search(query, search_type)
        self.results_label.text = '\n'.join([f'[ref={link}]{link}[/ref]' for link in results])

    def update_height(self, *args):
        self.results_label.height = self.results_label.texture_size[1]

class ParserApp(App):
    def build(self):
        return ParserPanel()

if __name__ == '__main__':
    ParserApp().run()
