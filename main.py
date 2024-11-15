from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from googlesearch import search

class SEOPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Заголовок
        self.title_label = Label(text='SEO Panel', font_size=24, bold=True, color=(0, 0, 1, 1), size_hint=(1, 0.1))
        self.add_widget(self.title_label)

        # Поисковая строка
        self.search_input = TextInput(hint_text="Введите запрос", multiline=False, size_hint=(1, 0.2))
        self.search_input.bind(focus=self.on_focus)
        self.add_widget(self.search_input)

        # Кнопка поиска
        self.search_button = Button(text="Поиск", size_hint=(1, 0.2), background_color=(0, 0, 1, 1))
        self.search_button.bind(on_press=self.perform_search)
        self.add_widget(self.search_button)

        # Окно вывода результатов
        self.results_label = Label(text="", size_hint=(1, 0.5))
        self.add_widget(self.results_label)

    def on_focus(self, instance, value):
        # Меняет цвет поисковой строки на оранжевый при фокусе
        if value:
            instance.background_color = (1, 0.5, 0, 1)
        else:
            instance.background_color = (1, 1, 1, 1)

    def perform_search(self, instance):
        # Выполняет поиск через Google API
        query = self.search_input.text
        results = []
        for url in search(query, num_results=10):
            results.append(url)
        self.results_label.text = "\n".join(results)

class SEOPanelApp(App):
    def build(self):
        return SEOPanel()

if __name__ == '__main__':
    SEOPanelApp().run()
