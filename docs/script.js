// Массив сайтов для поиска
const websites = [
  { name: 'OLX', url: 'https://www.olx.ua/list/q-' },
  { name: 'DOM.RIA', url: 'https://dom.ria.com/uk/search/?q=' },
  { name: 'LUN.ua', url: 'https://www.lun.ua/поиск/?q=' },
  { name: 'Address.ua', url: 'https://address.ua/search/?q=' },
  { name: 'Est.ua', url: 'https://www.est.ua/search/?q=' },
  { name: 'Flatfy.ua', url: 'https://flatfy.ua/поиск?q=' },
  { name: 'Mesto.ua', url: 'https://mesto.ua/search/?q=' },
  { name: 'Rieltor.ua', url: 'https://rieltor.ua/search/?q=' },
  { name: 'Realty.ua', url: 'https://www.realty.ua/search/?q=' },
  { name: '100realty.ua', url: 'https://100realty.ua/ru/object/search?text=' },
  { name: 'Blagovist.ua', url: 'https://blagovist.ua/search?text=' },
  { name: 'ROZETKA', url: 'https://rozetka.com.ua/search/?text=' },
  { name: 'Prom.ua', url: 'https://prom.ua/search?search_term=' },
  { name: 'Comfy', url: 'https://comfy.ua/ua/search/?q=' },
  { name: 'Eldorado', url: 'https://eldorado.ua/search/?q=' },
  { name: 'MOYO', url: 'https://www.moyo.ua/search/?q=' },
  { name: 'Stylus', url: 'https://stylus.ua/search?q=' },
  { name: 'Allo', url: 'https://allo.ua/ua/catalogsearch/result/?q=' },
  { name: 'Kasta', url: 'https://kasta.ua/market/?q=' },
  { name: 'Epicentr', url: 'https://epicentrk.ua/ua/search/?q=' },
  { name: 'Citrus', url: 'https://www.citrus.ua/search?query=' },
  { name: 'Foxtrot', url: 'https://www.foxtrot.com.ua/ru/search?query=' },
  { name: 'StopGame', url: 'https://stopgame.ru/search?query=' },
  { name: 'Игромания', url: 'https://www.igromania.ru/search/?q=' },
  { name: 'GameGuru', url: 'https://gameguru.ru/search/?q=' },
  { name: 'PlayGround', url: 'https://playground.ru/search?q=' },
  { name: 'ShowGamer', url: 'https://showgamer.com/?s=' },
  { name: 'ValGaming', url: 'https://valgaming.ru/?s=' },
  { name: 'GameFAQs', url: 'https://gamefaqs.gamespot.com/search?game=' },
  { name: 'Wikipedia', url: 'https://ru.wikipedia.org/wiki/Служебная:Search?search=' }
];

// Обработчик события для кнопки "Поиск"
document.getElementById('search-button').addEventListener('click', function() {
  const query = document.getElementById('search-box').value.trim();
  if (query !== '') {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<p>Результаты поиска для "<strong>${query}</strong>":</p><ul></ul>`;
    const ul = resultsDiv.querySelector('ul');

    // Определяем количество ссылок для отображения
    const totalWebsites = websites.length;
    const minLinks = 3;
    const maxLinks = 20;
    let numberOfLinks = totalWebsites;

    if (totalWebsites < minLinks) {
      numberOfLinks = totalWebsites;
    } else if (totalWebsites > maxLinks) {
      numberOfLinks = maxLinks;
    }

    websites.slice(0, numberOfLinks).forEach(site => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = site.url + encodeURIComponent(query);
      a.target = '_blank';
      a.textContent = `Поиск на ${site.name}`;
      li.appendChild(a);
      ul.appendChild(li);
    });
  } else {
    alert('Пожалуйста, введите запрос для поиска.');
  }
});
