from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set("graphics", "width", 560)
Config.set("graphics", "height", 900)
Config.set("graphics", "borderless", '1')
Config.set("graphics", "always_on_top", '1')
Config.write()
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar, MDSnackbar
from ctypes import windll, c_int64
from win32api import GetMonitorInfo, MonitorFromPoint
windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
from threading import Thread
from kivy.clock import mainthread
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import mind
import tts
import stt
import prefs_manager



class ChatScreen(MDScreen):
    pass


class SettingsScreen(MDScreen):
    pass


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    icon = 'assets/other/icon.ico'
    title = 'Sarah - Copilot for Windows'
    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    work_area = monitor_info.get("Work")
    Window.top = work_area[3] - Window.height
    Window.left = work_area[2] - Window.width
    username = mind.get_username()
    speech_service_started = False
    def stt_service(self, value):
        if not self.speech_service_started:
            if value:
                self.root.get_screen('chat').ids.listen_notification.opacity = 1
                self.speech_service_started = True
                self.stt_thread = Thread(target=stt.hotword_detection,
                                         args=[stt.q_callback, self.root.get_screen('chat').ids.field,
                                               self.root.get_screen('chat').ids.send])
                self.stt_thread.daemon = True
                self.stt_thread.start()

        else:
            self.root.get_screen('chat').ids.listen_notification.opacity = 0
            if not value:
                self.speech_service_started = False



    def on_start(self):
        self.init_prefs()




    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "200"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        return Builder.load_file('main.kv')

    def clear_history(self):
        for i in range(1, len(self.root.get_screen('chat').ids.chat.children)):
            self.root.get_screen('chat').ids.chat.remove_widget(self.root.get_screen('chat').ids.chat.children[1])
            mind.clear_history()
    def init_prefs(self):
        if (prefs_manager.get('provider') == None):
            prefs_manager.write('provider', mind.get_providers()[0])
        if (prefs_manager.get('voice_recognition') == None):
            prefs_manager.write('voice_recognition', False)
        if (prefs_manager.get('voice_synthesis') == None):
            prefs_manager.write('voice_synthesis', False)
        if prefs_manager.get('path_to_vosk_model') != None:
            is_valid = stt.check_model(prefs_manager.get('path_to_vosk_model'))
            if is_valid:
                self.root.get_screen('settings').ids.voice_recognition.disabled = False
            else:
                self.root.get_screen('settings').ids.voice_recognition.disabled = True
                self.root.get_screen('settings').ids.voice_recognition.active = False
                self.root.get_screen('settings').ids.path_to_vosk_model.text = ""
                prefs_manager.write('path_to_vosk_model', None)
                prefs_manager.write('voice_recognition', False)
        else:
            self.root.get_screen('settings').ids.voice_recognition.disabled = True
            self.root.get_screen('settings').ids.voice_recognition.active = False
            self.root.get_screen('settings').ids.path_to_vosk_model.text = ""
            prefs_manager.write('path_to_vosk_model', None)
            prefs_manager.write('voice_recognition', False)
        if prefs_manager.get('voice_recognition') == True:
            self.root.get_screen('settings').ids.voice_recognition.active = True
            self.root.get_screen('chat').ids.listen_notification.opacity = 1
            self.stt_service(True)
        else:
            self.root.get_screen('settings').ids.voice_recognition.active = False
            self.root.get_screen('chat').ids.listen_notification.opacity = 0
            self.stt_service(False)

        if prefs_manager.get('voice_synthesis') == True:
            self.root.get_screen('settings').ids.voice_synthesis.active = True
        else:
            self.root.get_screen('settings').ids.voice_synthesis.active = False

        if prefs_manager.get('path_to_vosk_model') is not None:
            self.root.get_screen('settings').ids.path_to_vosk_model.text = prefs_manager.get('path_to_vosk_model')
        self.root.get_screen('settings').ids.provider_button.text = prefs_manager.get('provider')

    @mainthread
    def add_chat_item(self, sender, text):

        error = False
        self.root.get_screen('chat').ids.field.text = ""
        item = MDCard(orientation='vertical', padding='14dp', spacing='10dp', adaptive_height=True)
        sender_label = MDLabel(text=sender, theme_text_color='Custom', adaptive_height=True, font_style="Caption")
        message_label = MDLabel(text=text, theme_text_color='Custom', adaptive_height=True, font_style="Body1")
        item.height = message_label.height + sender_label.height
        item.add_widget(sender_label)
        item.add_widget(message_label)
        if sender == "error":
            error = True
        if text == '':
            text = "Произошла ошибка:\nполучен пустой ответ"
            error = True
        if error:
            message_label.text = text
            item.md_bg_color = "#93000a"
            sender_label.text_color = "#ffdad6"
            message_label.text_color = "#ffdad6"
            item.remove_widget(sender_label)
            self.root.get_screen('chat').ids.chat.add_widget(item, 1)
            self.root.get_screen('chat').ids.scrollview.scroll_to(item)
            self.is_typing(False)
            return

        if sender == self.username:
            item.md_bg_color = "#272429"
            sender_label.text_color = "#cbc4cf"
            message_label.text_color = "#cbc4cf"
        else:
            if prefs_manager.get('voice_synthesis') == True:
                tts_thread = Thread(target=tts.say, args=[text])
                tts_thread.daemon = True
                tts_thread.start()
            self.is_typing(False)
            item.md_bg_color = "#4f378a"
            sender_label.text_color = "#ebddff"
            message_label.text_color = "#ebddff"

        self.root.get_screen('chat').ids.chat.add_widget(item, 1)
        self.root.get_screen('chat').ids.scrollview.scroll_to(item)

    @mainthread
    def is_typing(self, v):
        if v:
            self.root.get_screen('chat').ids.typing_animation.opacity = 1
        else:
            self.root.get_screen('chat').ids.typing_animation.opacity = 0

    def get_ai_response(self, text):
        self.is_typing(True)
        try:
            resource = mind.ai_answer(text)
            self.add_chat_item("Sarah", resource)
        except Exception as e:
            self.is_typing(False)
            self.add_chat_item("error", "Произошла ошибка:\n" + str(e))
        self.root.get_screen('chat').ids.disable = False

    def send_callback(self):
        text = self.root.get_screen('chat').ids.field.text
        self.root.get_screen('chat').ids.disable = True
        self.add_chat_item(self.username, text)
        t = Thread(target=self.get_ai_response, args=[text])
        # set daemon to true so the thread dies when app is closed
        t.daemon = True
        # start the thread
        t.start()

    def toolbar_callback(self):
        print('pressed')
        if self.root.current == "chat":
            self.root.current = "settings"
            self.root.transition.direction = "left"
        else:
            self.root.current = "chat"
            self.root.transition.direction = "right"

    def set_provider(self, provider):
        prefs_manager.write('provider', provider)
        self.root.get_screen('settings').ids.provider_button.text = provider
        self.menu.dismiss()

    def update_tts(self, value):
        prefs_manager.write('voice_synthesis', value)

    def update_stt(self, value):
        prefs_manager.write('voice_recognition', value)
        self.stt_service(value)
        self.init_prefs()
        if not value:
            self.root.get_screen('chat').ids.listen_notification.opacity = 0
        else:
            self.root.get_screen('chat').ids.listen_notification.opacity = 1
    def set_provider_menu(self):
        menu_items = [
            {
                "text": str(i),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.set_provider(x),
            } for i in mind.get_providers()
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.get_screen('settings').ids.provider_button.parent,
            items=menu_items,
            width_mult=4,
            md_bg_color="#49454e"
        )
        self.menu.open()

    def set_model(self):
        path = prefs_manager.open_folder_dialog()
        if path is not None and len(path) == 1:
            path = path[0]
            print(path)
            if stt.check_model(path):
                prefs_manager.write('path_to_vosk_model', path)
                self.root.get_screen('settings').ids.path_to_vosk_model.text = path
                snack = MDSnackbar()
                snack.duration = 3
                snack.md_bg_color = "#6cfe9d"
                self.root.get_screen('settings').ids.voice_recognition.disabled = False
                snack.add_widget(
                    MDLabel(text="Модель инициализирована!", halign="left", theme_text_color="Custom",
                            text_color="#00210c"))

                snack.open()
            else:
                prefs_manager.write('path_to_vosk_model', None)
                self.root.get_screen('settings').ids.voice_recognition.disabled = True
                self.root.get_screen('settings').ids.voice_recognition.active = False
                self.root.get_screen('settings').ids.path_to_vosk_model.text = ""
                prefs_manager.write('path_to_vosk_model', None)
                prefs_manager.write('voice_recognition', False)
                self.stt_service(False)
                snack = MDSnackbar()
                snack.duration = 3
                snack.md_bg_color="#93000a"
                snack.add_widget(MDLabel(text="Ошибка инициализации модели...", halign="left", theme_text_color="Custom", text_color="#ffdad6"))

                snack.open()
if __name__ == '__main__':
    MainApp().run()
