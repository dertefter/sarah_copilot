import threading
import time
from playsound import playsound
import requests
import vosk
import sys
import sounddevice as sd
import queue
import json
from kivy.clock import mainthread
import prefs_manager
model = vosk.Model("assets/small_ru")
samplerate = 16000
device = 1

is_record = False

q = queue.Queue()
freq = 44100
duration = 2


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def hotword_detection(callback, textfield, button):
    is_record = False
    print("hotword detection started")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback) as input_stream:

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            if prefs_manager.get('voice_recognition') == False:
                print("voice recognition disabled")
                break
            data = q.get()
            if rec.AcceptWaveform(data):
                get = json.loads(rec.Result())["text"]
                print(get)
                if not is_record:
                    if len(get) >= 4 and ((get[0] == "с" or get [0] == "ш") and get[2] == "р"):
                        print("hotword detected")
                        is_record = True
                        listen_animation(True, textfield, button)
                else:
                    time.sleep(1.2)
                    stt_result_to_ui(get, textfield, button)
                    is_record = False
                    listen_animation(False, textfield, button)


@mainthread
def stt_result_to_ui(text, textfield, button):
    if(text == ''):
        notify('cancel')
        return
    capitalise = text[0].upper() + text[1:]
    textfield.text = capitalise
    button.trigger_action(0)

@mainthread
def listen_animation(v, field, button):
    if v:
        field.text = "Слушаю..."
        button.icon = "microphone"
        button.disabled = True
        field.parent.md_bg_color = "#4a4458"
        notify('listen')
    else:
        button.icon = "send"
        button.disabled = False
        field.parent.md_bg_color = "#272429"

def notify(arg):
    sound = 'assets/audio/listen.wav'
    if arg == 'listen':
        sound = 'assets/audio/listen.wav'
    elif arg == 'cancel':
        sound = 'assets/audio/cancel.wav'
    threading.Thread(target=playsound, args=(sound,)).start()