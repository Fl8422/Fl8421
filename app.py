from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'links': []})

    links = google_search(query)
    return jsonify({'links': links})

def google_search(query):
    driver_path = 'path/to/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path)
    links = []

    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
        links = [result.get_attribute('href') for result in results]
    finally:
        driver.quit()

    return links

if __name__ == '__main__':
    app.run(debug=True)
