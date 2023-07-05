import json
import ctypes
import windialog as wd

def get(name):
    with open('prefs.json') as f:
        data = json.load(f)
        if name in data:
            return data[name]
        else:
            return None

def write(name, value):
    with open('prefs.json') as f:
        data = json.load(f)
        data[name] = value
        with open('prefs.json', 'w') as f:
            json.dump(data, f)
def open_folder_dialog():
    return wd.getdir()