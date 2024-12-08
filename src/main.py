from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from search_handler import perform_search

class ParserPanel(BoxLayout):
    def search(self, query, search_type):
        results = perform_search(query, search_type)
        self.ids.results.text = "\n".join(results)

class ParserPanelApp(App):
    def build(self):
        return ParserPanel()

if __name__ == "__main__":
    ParserPanelApp().run()
