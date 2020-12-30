from glob import glob
from time import time

import pandas as pd
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


SILENCE_THRESH = -45  # Consider a chunk silent if it's quieter than -16 dBFS.

mockingbird = None
def split_song(path, chapter):
    dir_name = f'pronunciation/audio_chunks/{chapter}'
    if os.path.exists(dir_name):
        return
    song = AudioSegment.from_mp3(path)
    chunks = split_on_silence(song, min_silence_len=200, silence_thresh=SILENCE_THRESH)
    print(len(chunks))

    if len(chunks):
        os.makedirs(dir_name, exist_ok=True)
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)
        audio_chunk = silence_chunk + chunk + silence_chunk

        audio_chunk.export(f'{dir_name}/{chapter}_{i}.mp3', bitrate="192k", format="mp3")
    return len(chunks)


dir_name = '/Users/vborovic/Google Drive/English/Pronunciation/Self_Study/English phonetics and pronunciation practice'
files = glob(dir_name + '/*/*')
for path in files:
    s = time()
    chapter = os.path.splitext(os.path.basename(path))[0]
    try:
        r = split_song(path, chapter)
        print(chapter, time() - s)
    except:
        print('error for ', chapter)
#
# chapter_to_total_words = df.groupby('chapter').chapter.count().to_dict()
# for ch, t in chapter_to_total_words.items():
#     if ch != '3.13.7':
#         continue
#     s = time()
#     c = ch.split('.')[0]
#     path = f'{dir_name}/Chapter {c}/{ch}.mp3'
#     print(path)
#     r = split_song(path, ch)
#     print(r, t, r == t)
#     print(time() - s)
#     break
