[app]

# Имя вашего приложения
title = SEO Panel

# Название пакета (должно быть уникальным)
package.name = seo_panel

# Домен пакета (обратный стиль домена)
package.domain = org.seopanel

# Версия приложения
version = 1.0

# Исходный файл, содержащий код приложения
source.main = main.py

# Папка, содержащая исходный код
source.dir = .

# Включенные модули Python
requirements = python3,kivy,googlesearch-python

# Скрытие консоли (включить для релизов)
log_level = 2

# Разрешения для Android
android.permissions = INTERNET

# Минимальная версия API Android (API 21 соответствует Android 5.0)
android.minapi = 21

# Текст лицензии
license = MIT

# Текст авторства
author = Your Name

# Ключевые слова
description = Приложение для выполнения SEO-запросов через Google API.

# Главный модуль для запуска
entrypoint = main.py

# Иконка приложения
icon.filename = icon.png

# Сплэш-экран (опционально)
presplash.filename = presplash.png

# Поддерживаемые языки
android.locales = en,ru

# Отключить сжатие для указанных расширений (опционально)
android.no-compile-pyo = True

# Включение дополнительного вывода для отладки
debug = False

# Целевые платформы
android.archs = arm64-v8a, armeabi-v7a

# Формат файла .apk (debug/release)
build_mode = debug

# Установить имя APK
android.apk_name = SEO_Panel

# Архитектуры для поддержки (по умолчанию все поддерживаемые)
android.add_archs = arm64-v8a,armeabi-v7a

# Дополнительные файлы или папки для включения
android.add_src = .

# Указать Java SDK для сборки (если требуется)
android.sdk_path = /data/data/com.termux/files/home/.buildozer/android/platform/android-sdk

# Указать NDK для сборки (если требуется)
android.ndk_path = /data/data/com.termux/files/home/.buildozer/android/platform/android-ndk-r21e

# Включить поддержку многопоточности (опционально)
p4a.branch = release

[buildozer]
# Логирование и отладка
warn_on_root = 1
verbose = 0
