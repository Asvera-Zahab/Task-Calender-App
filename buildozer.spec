[app]

# Basic app info
title = Task Calendar
package.name = taskcalendar
package.domain = com.yourname

source.dir = .
source.include_exts = py,png,jpg,kv,ttf,atlas
version = 0.1

# App icon shown on the phone's home screen / app drawer.
icon.filename = %(source.dir)s/assets/icon/icon.png

# Only kivy is needed - everything else is Python standard library (sqlite3, datetime, calendar).
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# No special permissions needed: the app is fully offline and only
# writes to its own private app storage.
android.permissions =

android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

# Keep old data (tasks) if the user updates the app later.
android.wipe_data = 0

[buildozer]
log_level = 2
warn_on_root = 1
