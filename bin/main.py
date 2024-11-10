import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from threading import Thread

class ParserPanel(BoxLayout):
    search_box = ObjectProperty(None)
    results = ObjectProperty(None)

    def search_google(self):
        query = self.search_box.text.strip()
        if not query:
            self.display_results("Пожалуйста, введите поисковый запрос.")
            return
        # Запуск поиска в отдельном потоке, чтобы не блокировать UI
        Thread(target=self.fetch_results, args=(query,)).start()

    def fetch_results(self, query):
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }
            response = requests.get(
                f"https://www.google.com/search?q={query}",
                headers=headers,
                timeout=10
            )
            if response.status_code != 200:
                self.display_results(f"Ошибка: Статус код {response.status_code}")
                return

            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all('h3')
            results_text = ""
            for idx, result in enumerate(results, start=1):
                title = result.get_text()
                link_tag = result.find_parent('a')
                link = link_tag['href'] if link_tag else "Ссылка недоступна"
                results_text += f"{idx}. {title}\n{link}\n\n"

            if not results_text:
                results_text = "Результаты не найдены."

            self.display_results(results_text)
        except Exception as e:
            self.display_results(f"Ошибка при поиске: {str(e)}")

    @mainthread
    def display_results(self, text):
        self.results.text = text

class ParserPanelApp(App):
    def build(self):
        self.title = "Parser Panel"
        return ParserPanel()

if __name__ == "__main__":
    ParserPanelApp().run()
