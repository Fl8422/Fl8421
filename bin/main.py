from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest

class ParserPanel(BoxLayout):
    def search_google(self):
        query = self.ids.search_box.text.strip()
        if query:
            # Здесь вы можете отправить запрос на ваш сервер для парсинга
            # Пример использования API (замените URL на ваш сервер)
            api_url = f"https://yourserver.com/api/search?q={query}"
            UrlRequest(api_url, on_success=self.on_success, on_failure=self.on_failure)
    
    def on_success(self, request, result):
        # Обработка успешного ответа от сервера
        self.ids.results.text = result.get('data', 'No results found.')
    
    def on_failure(self, request, result):
        # Обработка ошибки запроса
        self.ids.results.text = "Error fetching results."

class ParserPanelApp(App):
    def build(self):
        self.title = "Parser Panel"
        return ParserPanel()

if __name__ == "__main__":
    ParserPanelApp().run()
