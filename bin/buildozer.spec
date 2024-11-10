[app]

# (str) Title of your application
title = Parser Panel

# (str) Package name
package.name = parser_panel

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py is located
source.dir = bin

# (str) Main .py file
source.main = main.py

# (list) Source files to include (let empty to include all)
source.include_exts = py, kv, png

# (list) Application requirements
requirements = python3, kivy, requests, beautifulsoup4

# (str) Icon of the application
icon.filename = assets/zoom.png

# (list) Permissions
android.permissions = INTERNET

# (str) Orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (str) Path to custom source for the icon
# icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (portrait, landscape or all)
# orientation = portrait

# (int) Target API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 23b

# (str) Python version to use
# python.version = 3.8

# (bool) Use --private data storage (True) or --dir public storage (False)
private_storage = True

# (str) Android entry point, default is ok
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is 'import android' which corresponds to 'Theme.NoTitleBar'
# android.theme = '@android:style/Theme.NoTitleBar'

# (list) Patterns to exclude from the package
# android.exclude_patterns = license, images/*.jpg

# (str) Path to a custom source for the icon
# icon.filename = %(source.dir)s/icon.png

# (str) Path to a custom source for the splash screen
# splash.filename = %(source.dir)s/splash.png

# (int) Time to display the splash screen (in milliseconds)
# splash.duration = 3000

# (bool) Enable the debug mode
# debug = False

# (bool) Enable the log
# log_level = 2

# (bool) Enable the window's title bar
# window.title = Parser Panel

# (str) Supported orientation (portrait, landscape or all)
# orientation = portrait

# (str) Path to custom source for the icon
# icon.filename = %(source.dir)s/icon.png
