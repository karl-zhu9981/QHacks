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
        csvRow = df.loc[df['audio_filename'] == '/'.join([year, songFile])]
        assert csvRow['year'].to_list()[0] == int(year), 'CSV year is incorrect'
        split = csvRow['split'].to_list()
        assert len(split) == 1, 'CSV train/test split is incorrect'
        split = split[0]
        if not isdir('{}/{}/{}'.format(dataFolder, split, year)): makedirs('{}/{}/{}'.format(dataFolder, split, year))
        print('{} of {}\t{}\t{}'.format(i + 1, len(glob(yearFolder + '\*.wav')), split, song))

        if any(list(map(lambda name: NotExists('{}/{}/{}/{}'.format(dataFolder, split, year, songFile[:-4]), name),
                        ['Mels', 'Onsets', 'Offsets', 'Actives', 'Volumes']))):
            ######################################################################################################
            # From https://github.com/tensorflow/magenta/blob/master/magenta/music/audio_io.py
            
            nativeRate, y = readWave(song)
            if y.dtype == np.int16: y = int16_samples_to_float32(y)
            elif y.dtype != np.float32: raise AudioIOError('WAV file not 16-bit or 32-bit float PCM, unsupported')
            
            if y.ndim == 2 and y.shape[1] == 2: y = lbr.to_mono(y.T)
            if nativeRate != rate: y = lbr.resample(y, nativeRate, rate)
            samples = lbr.util.normalize(y)
            sequence = apply_sustain_control_changes(midi_file_to_note_sequence(song[:-3] + 'midi'))
            roll = sequence_to_pianoroll(sequence, 1 / lbr.frames_to_time(1, rate), 21, 108,
                                         onset_length_ms=32, offset_length_ms=32, onset_mode='length_ms')
            splits = [0, sequence.total_time] if split == 'test' else \
                find_split_points(sequence, samples, rate, minSecs, maxSecs)

            mels, onsets, offsets, actives, volumes = [], [], [], [], []
            for i, (start, end) in enumerate(zip(splits[:-1], splits[1:])):
                print('\tFragment {} of {}'.format(i + 1, len(splits) - 1), end='\t')
                if end - start < minSecs:
                    if i not in [0, len(splits) - 2]: print('WARNING: ', end='')
                    print('Skipping short sequence < {} seconds'.format(minSecs))
                    continue
                
                # Resampling in crop_wav_data is really slow, and we have already done it once, avoid doing it twice:
                newMels = lbr.power_to_db(lbr.feature.melspectrogram(samples if start == 0
                        and end == sequence.total_time else crop_samples(samples, rate, start, end - start),
                    rate, n_mels=229, fmin=30, htk=True).astype(np.float32).T).astype(np.float16)
                newOnsets, newOffsets, newActives, newVolumes = map(lambda arr:arr[
                        lbr.time_to_frames(start + lbr.frames_to_time(1, rate) / 2, rate) :
                        lbr.time_to_frames(  end + lbr.frames_to_time(1, rate) / 2, rate) + 1],
                    [roll.onsets, roll.offsets, roll.active, roll.onset_velocities])
                if split != 'test':
                    if len(newOnsets) == len(newMels) + 1: newOnsets, newOffsets, newActives, newVolumes \
                        = newOnsets[:-1], newOffsets[:-1], newActives[:-1], newVolumes[:-1]
                    elif len(newMels) == len(newOnsets) + 1: newMels = newMels[:-1]
                elif len(newOnsets) < len(newMels): newMels = newMels[:len(newOnsets)]
                assert split == 'test' or len(newOnsets) == len(newMels), \
                    'Spectrogram duration is different from piano rolls durations'

                if not newOnsets.sum():
                                    if i not in [0, len(splits) - 2]: print('WARNING: ', end='')
                                    print('Skipping empty sequence')
                                    continue
                                try: assert melsMinMin < newMels.min() < melsMinMax and melsMeanMin < newMels.mean() < melsMeanMax \
                                    and melsMaxMin < newMels.max() < melsMaxMax, 'Wrong mels decibels range'
                                except:
                                    if i == len(splits) - 2 and newMels.min() == newMels.mean() == newMels.max() == -100:
                                        print('WARNING: Skipping strange sequence with all mels = -100 Db')
                                        continue
                                    else:
                                        print(newMels.min(), newMels.mean(), newMels.max())
                                        raise

                                ########################################################################################################
                                # Unfortunately, magenta.music.sequences_lib.extract_subsequence does not take the correct time interval
                                # So, we have to manually remove notes which started before the interval:
                                for note in newActives[0].nonzero()[0]:
                                    for i, act in enumerate(newActives):
                                        if newOnsets[i][note] or not act[note]: break
                                        newActives[i][note] = 0
                                ########################################################################################################

                                if split != 'test': newMels, newOnsets, newOffsets, newActives, newVolumes = map(
                                    lambda arr: np.pad(arr, [(0, nFrames - len(arr)), (0, 0)], 'minimum' if arr is newMels \
                                    else 'constant'), [newMels, newOnsets, newOffsets, newActives, newVolumes])
                                assert newMels.shape[:-1] == newOnsets.shape[:-1] == newOffsets.shape[:-1]        \
                                        == newActives.shape[:-1] == newVolumes.shape[:-1]                          \
                                    and newOnsets.shape == newOffsets.shape == newActives.shape == newVolumes.shape \
                                    and newOnsets.shape[1] == 88 and newMels.shape[1] == 229, 'Wrong data shape'
                                mels, onsets, offsets, actives, volumes = map(lambda arr, newArr: arr + [newArr],
                                    [mels, onsets, offsets, actives, volumes], [newMels, newOnsets, newOffsets, newActives, newVolumes])
                                print()
            
                            for name, arr in zip(['Mels', 'Onsets', 'Offsets', 'Actives', 'Volumes'],
                                                 [mels, onsets, offsets, actives, volumes]):
                                np.save('{}/{}/{}/{} {}'.format(dataFolder, split, year, songFile[:-4], name), arr)

for splitFolder in ['train', 'test', 'validation']:
    for yearFolder in glob('{}\{}\*\\'.format(dataFolder, splitFolder)):
        yearFolder = int(yearFolder.split('\\')[2])
        print('\t', yearFolder, end='\n\n')
        mels, onsets, offsets, actives, volumes = [], [], [], [], []
        for i, [newMels, newOnsets, newOffsets, newActives, newVolumes] in enumerate(zip(*(
                glob('{}\{}\{}\*{}.npy'.format(dataFolder, splitFolder, yearFolder, arr))
                for arr in ['Mels', 'Onsets', 'Offsets', 'Actives', 'Volumes']))):
            song = newMels.split(' ')[0]
            assert song == newOnsets.split(' ')[0] == newOffsets.split(' ')[0] == newActives.split(' ')[0] \
                == newVolumes.split(' ')[0], 'Inconsistent number of numpy arrays'
            print('{} of {}'.format(i + 1, len(glob('{}\{}\{}\*Actives.npy'.format(
                dataFolder, splitFolder, yearFolder)))), end='\t')

            newMels, newOnsets, newOffsets, newActives, newVolumes = map(
                lambda arr: np.load(arr, allow_pickle=True), [newMels, newOnsets, newOffsets, newActives, newVolumes])
            mels, onsets, offsets, actives, volumes = map(lambda arr, newArr: (arr + newArr.tolist())
                if splitFolder == 'test' else np.vstack([arr, newArr]) if len(arr) else newArr,
                [mels, onsets, offsets, actives, volumes], [newMels, newOnsets, newOffsets, newActives, newVolumes])
            print(song)
        
        if splitFolder != 'test':
            mels, volumes = map(lambda arr: arr.astype(np.float16), [mels, volumes])
            onsets, offsets, actives = map(lambda arr: arr.astype(np.int8), [onsets, offsets, actives])
        for name, arr in zip(['Mels', 'Onsets', 'Offsets', 'Actives', 'Volumes'], [mels, onsets, offsets, actives, volumes]):
            np.save('{}/{}/{} {}'.format(dataFolder, splitFolder, yearFolder, name), arr)
        print('\n', len(actives), 'samples')
        
        melsFlat, volsFlat = map(np.concatenate, [mels, volumes])
        print('Mels decibels           in range [{:.0f} ... {:.0f} ... {:.0f}]'.format(
            melsFlat.min(), melsFlat.mean(), melsFlat.max()))
        assert melsMinMin < melsFlat.min() < melsMinMax and melsMeanMin < melsFlat.mean() < melsMeanMax \
            and melsMaxMin < melsFlat.max() < melsMaxMax, 'Wrong mels decibels range'

        print('Midi normalized volumes in range [{} ... {:.4f} ... {:.2f}]\n'.format(
            volsFlat.min(), volsFlat.mean(), volsFlat.max()))
        for arr in map(np.concatenate, [onsets, offsets, actives]): assert ((arr == 0) | (arr == 1)).all(), \
                'Onsets, offsets and actives must be only zeros and ones'
        assert volsFlat.min() == 0 and 0 < volsFlat.max() <= 1, 'Wrong normalized MIDI volumes range'

with File(dataFolder + '/Mels train.hdf5', 'w') as f: #, rdcc_nbytes=1024**3*4) as f: # 4 GB cache size
    for splitFolder in ['train', 'validation']:
        print(splitFolder)
        mels, onsets, offsets, actives, volumes = [], [], [], [], []
        for i, [newMels, newOnsets, newOffsets, newActives, newVolumes] in enumerate(zip(*(glob('{}\{}\*{}.npy'.format(
                dataFolder, splitFolder, arr)) for arr in ['Mels', 'Onsets', 'Offsets', 'Actives', 'Volumes']))):
            song = newOnsets.split(' ')[0]
            assert song == newOffsets.split(' ')[0] == newActives.split(' ')[0] == newVolumes.split(' ')[0], \
                'Inconsistent number of numpy arrays'
            print('{} of {}'.format(i + 1, len(glob('{}\{}\*Actives.npy'.format(
                dataFolder, splitFolder)))), end='\t')

            newMels, newOnsets, newOffsets, newActives, newVolumes = map(
                lambda arr: np.load(arr, allow_pickle=True), [newMels, newOnsets, newOffsets, newActives, newVolumes])
            
            if splitFolder == 'train':
                # Memory Error, so at first collect data in resisable HDF5-file, then it can be re-saved to NumPy-file
                if not mels: mels = f.create_dataset('Mels', data=newMels,
                    maxshape=(None, newMels.shape[1], newMels.shape[2])) # chunks=True
                else:
                    mels.resize((len(mels) + len(newMels), mels.shape[1], mels.shape[2]))
                    mels[-len(newMels):] = newMels
            else: mels = (mels + newMels.tolist()) if splitFolder == 'test' \
                else np.vstack([mels, newMels]) if len(mels) else newMels

            onsets, offsets, actives, volumes = map(lambda arr, newArr: (arr + newArr.tolist())
                if splitFolder == 'test' else np.vstack([arr, newArr]) if len(arr) else newArr,
                [onsets, offsets, actives, volumes], [newOnsets, newOffsets, newActives, newVolumes])

  

        for name, arr in zip(['Mels', 'Onsets', 'Offsets', 'Actives', 'Volumes'], [mels, onsets, offsets, actives, volumes]):
            np.save('{}/{} {}'.format(dataFolder, name, splitFolder), arr)  
        melsFlat, volsFlat = map(np.concatenate, [mels, volumes])
        melsMin, melsMean, melsMax = np.min(melsFlat), np.mean(melsFlat), np.max(melsFlat)
        assert melsMinMin < melsMin < melsMinMax and melsMeanMin < melsMean < melsMeanMax \
            and melsMaxMin < melsMax < melsMaxMax, 'Wrong mels decibels range'

        print('Midi normalized volumes in range [{} ... {:.4f} ... {:.2f}]\n'.format(
            volsFlat.min(), volsFlat.mean(), volsFlat.max()))
        for arr in map(np.concatenate, [onsets, offsets, actives]): assert ((arr == 0) | (arr == 1)).all(), \
                'Onsets, offsets and actives must be only zeros and ones'
        assert volsFlat.min() == 0 and 0 < volsFlat.max() <= 1, 'Wrong normalized MIDI volumes range'