from pydub import AudioSegment
from pydub.silence import split_on_silence


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


SILENCE_THRESH = -60  # Consider a chunk silent if it's quieter than -16 dBFS.


def split_song(path, output_path):
    song = AudioSegment.from_mp3(path)
    chunks = split_on_silence(song, min_silence_len=300, silence_thresh=SILENCE_THRESH)
    print(len(chunks))

    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)
        audio_chunk = silence_chunk + chunk + silence_chunk

        audio_chunk.export(f'{output_path}{i}.mp3', bitrate="192k", format="mp3")
    return len(chunks)

#
# split_song('/Users/vborovic/Downloads/game_sfx.mp3', '/Users/vborovic/Downloads/')
#
#
# import shutil
# import os
# os.makedirs('/Users/vborovic/Downloads/w/')
# os.makedirs('/Users/vborovic/Downloads/s/')
# for i in range(88):
#     p = f'/Users/vborovic/Downloads/{i}.mp3'
#     if i%2 == 0:
#         dst = '/Users/vborovic/Downloads/w/'
#     else:
#         dst = '/Users/vborovic/Downloads/s/'
#     shutil.move(p, dst)
