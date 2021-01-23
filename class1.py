import sklearn as sk
import numpy as np
import pandas as pd
from magenta.music.audio_io      import int16_samples_to_float32, crop_samples
from magenta.music.midi_io       import midi_file_to_note_sequence
from magenta.music.sequences_lib import sequence_to_pianoroll, apply_sustain_control_changes
from magenta.models.onsets_frames_transcription.split_audio_and_label_data import find_split_points
from os.path import exists
from h5py import File
from glob import glob
import librosa as lbr 


dataFolder= ''
csvName=''
df = read_csv(dataFolder+ csvName, verbose= True)
fmin = 30
fmax= 11025
rate, minSecs, maxSecs, melsMinMin, melsMinMax, melsMeanMin, melsMeanMax, melsMaxMin, melsMaxMax \
    = 16_000, 1, 5, -40, -40, -0, -0, 40, 40
nFrames = lbr.time_to_frames(maxSecs, rate) + 1

for yearFolder in glob(dataFolder+'\*\\'):
    if yearFolder.split('\\')[1] in ['train', 'test', 'validation']: continue
    for i,song in enumerate(glob(yearFolder + '\*.wav')):
        year,songFile = song.split('\\')[1:]
