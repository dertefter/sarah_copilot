# Sarah - Copilot for Windows 11
[![English](https://img.shields.io/badge/russian%20-%20language?label=language&color=922)](README.md)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffffff) ![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)


![header](assets/other/preview.png)
An attempt to create a Copilot for Windows. The project is based on [gpt4free](https://github.com/xtekky/gpt4free).

## Project Description

The project uses the gpt4free library to work with the ChatGPT model. If a simple text response is not sufficient, the program can generate Python code and then execute that code to obtain the result.

In fact, this approach allows ChatGPT to perform almost any task on your computer. For example, you can ask ChatGPT to open a website or a program, find out the exact time and date, or create and delete files.

> Important: The program has unpredictable behavior due to the characteristics of the ChatGPT model. Please exercise caution when interacting with it and do not trust it to perform any tasks that could harm your computer.

## Application Features

1. Interaction with ChatGPT: Users can ask questions or request specific tasks using text queries.
2. Code Compilation and Execution: The application recognizes code in the response from ChatGPT, saves it to the `execute.py` file, and executes the received code, displaying the execution result.
3. Voice Input: The application supports voice input after the activation phrase "Sarah". The [vosk](https://alphacephei.com/vosk/) library is used for voice processing. To use this feature, you need to download the models [here](https://alphacephei.com/vosk/models), unpack them to a convenient location, and specify the path to the model in the application settings.
4. Speech Synthesis: The application can vocalize the results using the Windows speech synthesizer.

## Installation
```
pip install -r requirements.txt
```

## Running
```
python main.py
```

## Screenshots
<div style="height: 50%">

![screenshot](assets/screenshots/1.png)
![screenshot](assets/screenshots/2.png)
![screenshot](assets/screenshots/3.png)

</div>

## Important
> This project is created for educational purposes. The author is not responsible for your actions. Use it at your own risk.

## Acknowledgments
We would like to thank the following projects for their contributions to the development of this application:
* [gpt4free](https://github.com/xtekky/gpt4free)
* [vosk](https://alphacephei.com/vosk/)

## License
Distributed under the [MIT License](LICENSE.md)