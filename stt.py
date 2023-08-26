import threading
import time
import wave
import pyaudio
import vosk
import sys
import sounddevice as sd
import queue
import json
from kivy.clock import mainthread
import prefs_manager
import traceback

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

def check_model(path):
    try:
        print("Проверка модели...")
        model = vosk.Model(path)
        print("Модель корректна!")
        return True
    except:
        return False

def hotword_detection(callback, textfield, button, app):
    try:
        is_record = False
        model_path = prefs_manager.get("path_to_vosk_model")
        model = vosk.Model(model_path)

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                               channels=1, callback=q_callback):
            print(model)
            rec = vosk.KaldiRecognizer(model, samplerate)
            print("hotword detection started")
            while True:
                if not prefs_manager.get('voice_recognition'):
                    print("voice recognition disabled")
                    break
                data = q.get()
                if rec.AcceptWaveform(data):
                    get = json.loads(rec.Result())["text"]
                    print(get)
                    if not is_record:
                        if (len(get) >= 4 and ((get[0] == "с" or get [0] == "ш") and get[2] == "р")) or ("sarah" in get):
                            print("hotword detected")
                            is_record = True
                            listen_animation(True, textfield, button, app)
                    else:
                        time.sleep(1.2)
                        stt_result_to_ui(get, textfield, button)
                        is_record = False
                        listen_animation(False, textfield, button, app)
    except Exception:
        print(traceback.format_exc())
        print("Ошибка запуска распознавания речи")

@mainthread
def stt_result_to_ui(text, textfield, button):
    if(text == ''):
        notify('cancel')
        return
    capitalise = text[0].upper() + text[1:]
    textfield.text = capitalise
    button.trigger_action(0)

@mainthread
def listen_animation(v, field, button, app):
    if v:
        field.text = "Слушаю..."
        button.icon = "microphone"
        button.disabled = True
        field.parent.md_bg_color = app.theme_builder.get_color('primary')
        notify('listen')
    else:
        button.icon = "send"
        button.disabled = False
        field.parent.md_bg_color = app.theme_builder.get_color('surfaceContainer')

def play_wav_file(file_path):
    chunk = 1024

    # Open the WAV file
    wf = wave.open(file_path, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream to play the WAV file
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks and play them in the stream
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
def notify(arg):
    sound = 'assets/audio/listen.wav'
    if arg == 'listen':
        sound = 'assets/audio/listen.wav'
    elif arg == 'cancel':
        sound = 'assets/audio/cancel.wav'
    t = threading.Thread(target=play_wav_file, args=[sound])
    t.daemon = True
    t.start()