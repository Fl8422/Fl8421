[app]

# Название вашего приложения
title = Parser Panel

# Имя пакета
package.name = parser_panel

# Домен пакета (нужно для Android/iOS упаковки)
package.domain = org.example

# Каталог, где находится ваш main.py
source.dir = .

# Главный .py файл, точка входа в приложение
source.main = main.py

# Расширения файлов, которые будут включены
source.include_exts = py,kv,png,css

# Версия приложения
version = 0.1

# Автор приложения
author = Fl8421

# Иконка приложения
icon.filename = assets/icon.png

# Поддерживаемая ориентация (landscape, sensorLandscape, portrait, all)
orientation = portrait

# Указывает, будет ли приложение полноэкранным
fullscreen = 0

# Скрыть статусбар на Android
android.hide_statusbar = 1

# Разрешения, необходимые приложению
android.permissions = INTERNET

# Тема приложения
android.theme = '@android:style/Theme.NoTitleBar'

# Версия Android API
android.api = 31

# Минимальная поддерживаемая версия Android
android.minapi = 21

# Целевая версия Android
android.target = 31

# Требования (зависимости) приложения
requirements = python3,kivy,selenium,webdriver_manager

# Точка входа для Android
android.entrypoint = org.kivy.android.PythonActivity

# Включение режима отладки
debug = 1

# Сборка в режиме debug (0 - отключено, 1 - включено)
log_level = 2

# Дополнительные настройки можно добавить по мере необходимости

[buildozer]

# Уровень логирования (0: ничего, 1: ошибки, 2: предупреждения, 3: информация, 4: отладка)
log_level = 2

# Путь к каталогу сборки (по умолчанию .buildozer)
#build_dir = .buildozer

# Путь к каталогу для бинарных файлов (по умолчанию bin)
#bin_dir = bin
