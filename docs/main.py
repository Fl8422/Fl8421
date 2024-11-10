from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Загрузка интерфейса из parser.kv
Builder.load_file("parser.kv")

class ParserPanel(Widget):
    def search_google(self):
        query = self.ids.search_box.text  # Получаем текст из TextInput
        if query:
            # Запуск Selenium WebDriver для парсинга
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Режим без интерфейса
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(f"https://www.google.com/search?q={query}")

            # Пример получения результатов поиска
            results = driver.find_elements("css selector", "h3")
            output = "\n".join([result.text for result in results if result.text])
            self.ids.results.text = output or "No results found."
            driver.quit()

class ParserPanelApp(App):
    def build(self):
        self.title = "Parser Panel"
        return ParserPanel()

if __name__ == "__main__":
    ParserPanelApp().run()
