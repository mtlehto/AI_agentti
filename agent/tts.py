from gtts import gTTS
from pathlib import Path


def speak(t):
    Path("output").mkdir(exist_ok=True)
    gTTS(text=t,lang="fi").save("output/aamubriiffi.mp3")
