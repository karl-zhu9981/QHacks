from flask import Flask, request
import runpy
from time import sleep

app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
    runpy.run_path(file_path='\midiconversion\\ ', run_name= 'main')
    time.sleep(5)
    _notify()
    return

def _notify():
    res = requests.post('https://youtune-backend.web.app/')