# Sarah - Copilot для Windows 11
[![English](https://img.shields.io/badge/english%20-%20language?label=language&color=098)](README.ENG.md)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffffff) ![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)

![header](assets/other/preview.png)
Попытка создания своего Copilot для Windows. Проект основан на [gpt4free](https://github.com/xtekky/gpt4free).

## Описание проекта

Проект использует библиотеку gpt4free, чтобы работать с моделью ChatGPT. Если простой текстовый ответ не является достаточным, программа может генерировать код на языке Python, а затем получать результат выполнения этого кода.

Фактически, такой подход позволяет ChatGPT выполнять практически любые задачи на вашем компьютере. Например, вы можете попросить ChatGPT открыть какой-либо сайт, программу, узнать точное время и дату, создать или удалить файл.

> Важно: Программа имеет непредсказуемый характер из-за особенностей работы модели ChatGPT. Пожалуйста, будьте осторожны при обращении с ней, и не доверяйте ей выполнение каких-либо задач, которые могут нанести вред вашему компьютеру.

## Функции приложения

1. Взаимодействие с ChatGPT: Пользователь может задавать вопросы или просить выполнить определенные задачи с помощью текстовых запросов.
2. Компиляция и выполнение кода: Приложение распознает код в ответе от ChatGPT, сохраняет его в файл `execute.py` и выполняет полученный код, выводя результат выполнения.
3. Голосовой ввод: Приложение поддерживает голосовой ввод после фразы активации "Сара". Для обработки голоса используется библиотека [vosk](https://alphacephei.com/vosk/). Для использования данной функции необходимо скачать модели [здесь](https://alphacephei.com/vosk/models), распаковать их в удобное для вас место и указать путь к модели в настройках приложения.
4. Озвучивание результатов: Приложение может озвучивать результаты с помощью синтезатора речи Windows.

## Установка и запуск
```
git clone https://github.com/dertefter/sarah_copilot
```
```
cd sarah_copilot
```
```
python -m venv venv
```
```
call venv\Scripts\activate.bat
```
```
pip install -r requirements.txt
```
```
python main.py
```

## Скриншоты
<div style="height: 50%">

![screenshot](assets/screenshots/1.png)
![screenshot](assets/screenshots/2.png)
![screenshot](assets/screenshots/3.png)

</div>

## Важно
> Данный проект создан в ознакомительных целях. Автор не несёт ответственности за ваши действия. Используйте его на свой страх и риск.

## Благодарности
Мы благодарим следующие проекты за их вклад в разработку данного приложения:
* [gpt4free](https://github.com/xtekky/gpt4free)
* [vosk](https://alphacephei.com/vosk/)

## Лизцензия
Распространяется под лицензией [MIT](LICENSE.md)
