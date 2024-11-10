[app]

# Название вашего приложения
title = Parser Panel

# Имя пакета
package.name = parserpanel

# Домен пакета
package.domain = org.example.parserpanel

# Путь к исходному коду
source.dir = .

# Главный файл приложения
source.main = main.py

# Включаем необходимые расширения
source.include_exts = py,png,jpg,kv,atlas,css

# Версия приложения
version = 0.1

# Зависимости приложения
requirements = python3,kivy,selenium,webdriver_manager

# Иконка приложения
icon.filename = icon.png

# Поддерживаемая ориентация (portrait - вертикальная, landscape - горизонтальная)
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Скрыть статус-бар на Android
android.hide_statusbar = 1

# Разрешения на Android
android.permissions = INTERNET

# Минимальная версия API Android
android.minapi = 21

# Версия Android API для сборки
android.api = 31

# Версия Android SDK
android.sdk = 20

# Версия Android NDK
android.ndk = 23b

# Стиль приложения
android.theme = '@android:style/Theme.NoTitleBar'

# Используемые расширения файла
source.include_exts = py,png,jpg,kv,atlas,css

# Разрешение на интернет, чтобы Selenium мог подключаться
android.permissions = INTERNET

# Укажите путь к иконке
icon.filename = icon.png

# (bool) Укажите, нужно ли разрешить копирование приложения в буфер на Android
android.allow_backup = True

# (str) Платформа для сборки (apk)
android.build_format = apk

# (str) Поддерживаемые архитектуры (оставим стандартные)
android.arch = armeabi-v7a, arm64-v8a, x86, x86_64

# Максимальный уровень подробности вывода
log_level = 2

# Укажите, нужно ли очищать временные файлы перед сборкой
clean = False

[buildozer]

# Директория для вывода файлов сборки
build_dir = .buildozer

# Папка, в которой будет находиться APK
dist_dir = bin

# Логгирование в файл
log_file = buildozer.log
