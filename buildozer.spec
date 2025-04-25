[app]
title = Fire
package.name = firedetector
package.domain = org.fire.detection
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,opencv-python,numpy
orientation = portrait
fullscreen = 1
icon.filename = icon.png
android.permissions = CAMERA, INTERNET, ACCESS_FINE_LOCATION, WRITE_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 0
