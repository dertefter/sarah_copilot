
import os
import time

def answer():
    user_folder = os.path.expanduser('~')
    os.startfile(user_folder)
    time.sleep(2)
    os.system('taskkill /f /im explorer.exe')
    return "Папка пользователя открыта и затем закрыта."
