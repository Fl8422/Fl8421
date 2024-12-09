import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from googleapiclient.discovery import build
from kivy.uix.progressbar import ProgressBar
import time

kivy.require('2.1.0')

class ParserPanelApp(App):

    def build(self):
        self.api_key = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw'
        self.cse_id = '1277afbc49d06402d'

        self.root = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title Label
        self.title_label = Label(text="Parser Panel", font_size='24sp', color=(0, 0, 1, 1), bold=True)
        self.root.add_widget(self.title_label)
        
        # Search Input
        self.search_input = TextInput(hint_text='Enter your search query', multiline=False, size_hint_y=None, height=40)
        self.root.add_widget(self.search_input)
        
        # Spinner for search types
        self.search_type_spinner = Spinner(
            text='Standard Search',
            values=('Standard Search', 'Detailed Search', 'Time Search', 'Site Search'),
            size_hint_y=None,
            height=40
        )
        self.root.add_widget(self.search_type_spinner)

        # Search Button
        self.search_button = Button(text="Search", size_hint_y=None, height=40)
        self.search_button.bind(on_press=self.start_search)
        self.root.add_widget(self.search_button)

        # Progress Bar
        self.progress = ProgressBar(max=100, size_hint_y=None, height=20)
        self.root.add_widget(self.progress)

        # Result ScrollView
        self.result_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.result_box.bind(minimum_height=self.result_box.setter('height'))
        self.result_scroll = ScrollView(size_hint=(1, None), height=300)
        self.result_scroll.add_widget(self.result_box)
        self.root.add_widget(self.result_scroll)

        return self.root

    def start_search(self, instance):
        query = self.search_input.text
        search_type = self.search_type_spinner.text
        self.progress.value = 0
        self.result_box.clear_widgets()

        if search_type == 'Standard Search':
            self.perform_search(query)
        elif search_type == 'Detailed Search':
            self.perform_detailed_search(query)
        elif search_type == 'Time Search':
            self.perform_time_search(query)
        elif search_type == 'Site Search':
            self.perform_site_search(query)

    def perform_search(self, query):
        self.display_loading()
        self.fetch_search_results(query)

    def perform_detailed_search(self, query):
        self.display_loading()
        self.fetch_detailed_search(query)

    def perform_time_search(self, query):
        self.display_loading()
        self.fetch_time_search(query)

    def perform_site_search(self, query):
        self.display_loading()
        self.fetch_site_search(query)

    def display_loading(self):
        loading_label = Label(text="Searching...", size_hint_y=None, height=40)
        self.result_box.add_widget(loading_label)

    def fetch_search_results(self, query):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=query, cx=self.cse_id).execute()
        self.display_results(res)

    def fetch_detailed_search(self, query):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=query + " details", cx=self.cse_id).execute()
        self.display_results(res)

    def fetch_time_search(self, query):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=query + " last week", cx=self.cse_id).execute()
        self.display_results(res)

    def fetch_site_search(self, query):
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=f"site:{query}", cx=self.cse_id).execute()
        self.display_results(res)

    def display_results(self, res):
        if 'items' in res:
            for item in res['items']:
                link = item['link']
                title = item['title']
                snippet = item['snippet']

                result_label = Label(text=f"[{title}]({link})\n{snippet}", markup=True, size_hint_y=None, height=60)
                self.result_box.add_widget(result_label)
        else:
            self.result_box.add_widget(Label(text="No results found.", size_hint_y=None, height=40))

if __name__ == '__main__':
    ParserPanelApp().run()
