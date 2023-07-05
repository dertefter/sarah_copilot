import win32com.client as wincom

def say(text):
    speak = wincom.Dispatch("SAPI.SpVoice")
    speak.Speak(text)
