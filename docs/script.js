const { Builder, By, Key, until } = require('selenium-webdriver');

(async function searchGoogle() {
  // Инициализация драйвера для браузера (здесь используется Chrome)
  let driver = await new Builder().forBrowser('chrome').build();

  try {
    // Получаем поисковый запрос от пользователя
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    readline.question('Введите поисковый запрос: ', async (query) => {
      // Переходим на главную страницу Google
      await driver.get('https://www.google.com');

      // Вводим поисковый запрос и нажимаем Enter
      await driver.findElement(By.name('q')).sendKeys(query, Key.RETURN);

      // Ждем загрузки результатов
      await driver.wait(until.titleContains(query), 1000);

      // Получаем первые 20 результатов поиска
      let results = await driver.findElements(By.css('div.g'));
      results = results.slice(0, 20); // Ограничиваем до 20 результатов

      // Выводим результаты
      for (let result of results) {
        try {
          let titleElement = await result.findElement(By.css('h3'));
          let title = await titleElement.getText();
          let link = await result.findElement(By.css('a')).getAttribute('href');
          console.log(`- ${title}\n  ${link}\n`);
        } catch (err) {
          // Пропускаем результаты без заголовка или ссылки
          continue;
        }
      }

      // Закрываем интерфейс чтения
      readline.close();

      // Закрываем браузер
      await driver.quit();
    });
  } catch (error) {
    console.error('Произошла ошибка:', error);
    await driver.quit();
  }
})();
