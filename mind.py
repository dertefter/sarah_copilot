import g4f
import re
import getpass
import importlib
import execute
import traceback
import prefs_manager
show_pre = False
pattern_code = r"<python>(.*?)</python>"

init_message = '''
Ты - умный помошник для операционной системы Windows 11. Тебя зовут Сара.

Правила оформления твоих ответов:
Чтобы программа, в которой ты работаешь, поняла, что ты хочешь что-то сказать - оформи свою речь таким образом:
Пример твоего ответа ответа.

Ты можешь использовать Python для решения задач, поставленных пользователем, если это необходимо
Ты можешь пользоваться муделями, такими как pyautogui, getpass, cpuinfo, datatime, os. Пользоваться другими модулями не рекомеднуется
Чтобы выполнить какй-дибо код, оформи ответ следующим образом:
<python>
def answer():
    #твой код
    return result #result - это str
</python>
Функция всегда должна называться "answer". Есои её не будет - ты получешь ошибку. Ты просто пишешь функцию, результатом которой будет ответ.

'''
init_message2 = '''
Здравствуйте! Я ваш умный помощник для операционной системы Windows 11. Чем я могу вам помочь сегодня?)
'''

messages_array = [
    {"role": "user", "content": init_message},
    {"role": "assistant", "content": init_message2},
    {"role": "user", "content": "Открой меню пуск"},
    {'role': 'assistant',
     'content': '<python>\ndef answer():\n    import pyautogui\n    pyautogui.press(\'win\')\n    return "Я открыла меню Пуск))"\n</python>'},
    {"role": "user", "content": "Какой заряд батареи?"},
    {'role': 'assistant', 'content': '''<python>
def answer():
    import psutil
    battery = psutil.sensors_battery()
    percent = int(battery.percent)
    return f"Заряд батареи: {percent}%"
    </python>
    '''},

]

def clear_history():
    messages_array = [
        {"role": "user", "content": init_message},
        {"role": "assistant", "content": init_message2},
        {"role": "user", "content": "Открой меню пуск"},
        {'role': 'assistant',
         'content': '<python>\ndef answer():\n    import pyautogui\n    pyautogui.press(\'win\')\n    return "Я открыла меню Пуск))"\n</python>'},
        {"role": "user", "content": "Какой заряд батареи?"},
        {'role': 'assistant', 'content': '''<python>
    def answer():
        import psutil
        battery = psutil.sensors_battery()
        percent = int(battery.percent)
        return f"Заряд батареи: {percent}%"
        </python>
        '''},

    ]
def get_providers():
    return ["Ails",
            "You",
            "Bing",
            "Yqcloud",
            "Theb",
            "Aichat",
            "Bard",
            "Vercel",
            "Forefront",
            "Lockchat",
            "Liaobots",
            "H2o",
            "ChatgptLogin",
            "DeepAi",
            "GetGpt"]



def ai_answer(text):
    provider_pref = prefs_manager.get("provider")
    if provider_pref is None:
        prefs_manager.write("provider", get_providers()[0])
        provider_pref = prefs_manager.get("provider")
    provider = g4f.Provider.Forefront
    if provider_pref == "Ails":
        provider = g4f.Provider.Ails
    elif provider_pref == "You":
        provider = g4f.Provider.You
    elif provider_pref == "Bing":
        provider = g4f.Provider.Bing
    elif provider_pref == "Yqcloud":
        provider = g4f.Provider.Yqcloud
    elif provider_pref == "Theb":
        provider = g4f.Provider.Theb
    elif provider_pref == "Aichat":
        provider = g4f.Provider.Aichat
    elif provider_pref == "Bard":
        provider = g4f.Provider.Bard
    elif provider_pref == "Vercel":
        provider = g4f.Provider.Vercel
    elif provider_pref == "Forefront":
        provider = g4f.Provider.Forefront
    elif provider_pref == "Lockchat":
        provider = g4f.Provider.Lockchat
    elif provider_pref == "Liaobots":
        provider = g4f.Provider.Liaobots
    elif provider_pref == "H2o":
        provider = g4f.Provider.H2o
    elif provider_pref == "ChatgptLogin":
        provider = g4f.Provider.ChatgptLogin
    elif provider_pref == "DeepAi":
        provider = g4f.Provider.DeepAi
    elif provider_pref == "GetGpt":
        provider = g4f.Provider.GetGpt


    if text != "init":
        messages_array.append({"role": "user", "content": text})
    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo',
                                         messages=messages_array, stream=False, provider=provider)
    result = ""
    for part in response:
        result += part
    if show_pre:
        print("pre-result:", result)
    messages_array.append({"role": "assistant", "content": result})
    if "<python>" in result and "</python>" in result:
        match = re.search(pattern_code, result, re.DOTALL)
        if match:
            code_inside_tags = match.group(1)
            code = code_inside_tags
            with open("execute.py", "w", encoding='utf-8') as file:
                file.write(code)
            importlib.reload(execute)
            result = execute.answer()
    print(messages_array)

    return result


def get_username():
    import getpass
    username = getpass.getuser()
    return username
