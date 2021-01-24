from flask import Flask, request
import runpy
from time import sleep
from audio_to_midi import converter
app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
    process = converter.Converter(
            infile="default.wav",
            outfile="out.mid",
            time_window=5.0,
            activation_level=0.0,
            condense=False,
            condense_max=False,
            max_note_length=0,
            note_count=0,
            transpose=0,
            pitch_set=[],
            pitch_range=None,
            progress=None if args.no_progress else progress_bar.ProgressBar(),
            bpm=60,
        )
    process.convert()
    time.sleep(5)
    _notify()
    return

def _notify():
    res = requests.post('https://youtune-backend.web.app/')