
const buttons = document.querySelectorAll('.game-btn, .color-btn');
const colorButtons = document.querySelectorAll('.color-btn');

// Анимация нажатия на кнопки
buttons.forEach(button => {
    button.addEventListener('click', () => {
        button.style.backgroundColor = 'orange';
        setTimeout(() => {
            button.style.backgroundColor = 'gray';
        }, 1000);
    });
});

// Изменение цвета кнопок
colorButtons.forEach(button => {
    button.addEventListener('click', () => {
        const color = button.getAttribute('data-color');
        document.querySelectorAll('.game-btn').forEach(gameButton => {
            gameButton.style.backgroundColor = color;
        });
    });
});

// Функция для запуска игр
function startGame(game) {
    const gameArea = document.getElementById('game-area');
    gameArea.innerHTML = `<h2>Вы запустили игру: ${game}</h2>`;
}
