[app]
# Название приложения
title = Panel

# Имя пакета (замените "com.example.panel" на ваше имя пакета)
package.name = panel
package.domain = com.example

# Главный файл, который будет запускать приложение (например, app.py)
source.main = app.py

# Иконка приложения
icon.filename = res/free-icon-loupe-8668568.png

# (str) Платформы, на которых вы хотите запустить ваше приложение
# (android - для сборки APK файла)
source.include_exts = py,png,jpg,kv,atlas

# (list) Требуемые библиотеки python (зависимости вашего проекта)
requirements = python3, flask, requests, beautifulsoup4, googlesearch-python

# (str) Имя пакета для Android
package.name = panel
package.domain = com.example

# (str) Ориентация экрана
orientation = portrait

# (bool) Включить в apk все зависимости python
include_sqlite = False

# (str) Минимальная версия Android
android.api = 29
android.minapi = 21

# (int) Версия и версия кода приложения для Android
android.version_code = 1
android.version = 1.0

# (str) Архитектура процессора для Android
android.arch = armeabi-v7a

# (list) Поддержка языков (например, en, es, fr, ru)
presplash.filename = res/icon.png
fullscreen = 1

# (str) Пути к файлам и папкам, которые будут включены в APK
source.include_patterns = assets/*, templates/*, static/*

# (str) Директория, куда будет собираться APK
build_dir = build

# (bool) Включить logcat в режиме отладки
android.logcat_filter = *:S python:D
