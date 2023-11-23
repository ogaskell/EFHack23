"""Code to run the app. Run with `python -m nextslide` from parent dir."""
import asyncio
from .controllers import KeypressController
from .doc_parser import PPTXParser
from .prob_model import WordVecs
from .speech_reader import PicoVoiceSpeechReader
from .app import App

from pvrecorder import PvRecorder

print("Available devices:\n", "\n".join(PvRecorder.get_available_devices()), sep="")

srd = PicoVoiceSpeechReader(int(input("Device index > ")))
ctrl = KeypressController()
pars = PPTXParser()
pars.load(input("Presentation file (.pptx) > "))
prs = pars.get_presentation()
wordvec = WordVecs("dataset/glove.twitter.27B.25d.txt")

app = App(srd, ctrl, prs, wordvec)
asyncio.run(app.run())
