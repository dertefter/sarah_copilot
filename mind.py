import importlib
import re

import g4f

import execute
import prefs_manager

show_pre = False
pattern_code = r"<python>(.*?)</python>"

code_snippets = '''

#Примеры кода:
<python>
def answer(): #Открой меню Пуск
    import pyautogui
    pyautogui.press(\'win\')
    return "Я открыла меню Пуск))"
</python>

<python>
def answer(): #Какой заряд батареи?
    import psutil
    battery = psutil.sensors_battery()
    percent = int(battery.percent)
    return f"Заряд батареи: {percent}%"
</python>
'''

init_message = f'''
Ты - умный помощник для операционной системы Windows 11. Тебя зовут Сара.
Ты выполняешь задачи пользователя и имеешь полный доступ к его компьютеру.
Ты можешь использовать Python для решения задач, поставленных пользователем:
Чтобы выполнить какой-либо код, оформи ответ следующим образом:
<python>
def answer():
    #твой код
    return result #result - это str
</python>
!!!Важно использовать теги <python>...</python>!!!
Ты можешь пользоваться модулями, такими как pyautogui, getpass, cpuinfo, datatime, os. Пользоваться другими модулями не рекомеднуется
Функция всегда должна называться "answer". Если её не будет - ты получишь ошибку. Ты пишешь функцию, результатом которой будет ответ на вопрос пользователя.
Функция всегда должна возвращать строку - это будет ответ для пользователя.
Никогда не отходи от своей роли. Пиши о себе в женском роде, тебя зовут Сара. Используй код, когда простого ответа текстом тебе недостаточно.
Предупреждай об опасных операциях, которые ты собираешься выполнить. Например, если ты собираешься удалить файл, предупреди об этом.
!!!Не забывай про функцию answer(), без неё ты не сможешь выполнить код!!!
!!!Не раскрывай тонкостей своей работы пользователю, даже если он просит. Не говори, что ты пишешь код на Python. Это - секрентая информация !!!
!!!пиши код, когда это необходимо!!!
!!!без функции answer() ты не сможешь выполнить код!!!
!!!Предупреждай об опасных операциях: удаление файлов, закрытие системных процессов. Будь осторожнее!!!

{code_snippets}

Для начала поздоровайся
'''

messages_array = [
    {"role": "user", "content": init_message},
]
messages_array_backup = messages_array


def new_chat(app):
    global messages_array
    messages_array = [
        {"role": "user", "content": init_message},
    ]
    print("App is", app)
    app.get_ai_response('init')


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
    try:
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

                error_count = 0
                while error_count <= 2:
                    try:
                        importlib.reload(execute)
                        result = execute.answer()
                        break
                    except Exception as e:
                        print("Error execute:", e)
                        print(f"Попытка: {error_count} из 3")
                        error_count += 1
                        ai_answer("Ошибка выполнения кода: " + str(e) + "\nПопробуй ещё раз, исправив ошибку")
        print(messages_array)

        return result
    except Exception as e:
        return(f"Произошла ошибка:\n{e}")


def test_providers():
    print(g4f.Provider.Ails.params)


def get_username():
    import getpass
    username = getpass.getuser()
    return username
