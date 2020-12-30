import glob
import os
import re

import pandas as pd


# split_text()
#
# # #
# fls = [f for f in glob.glob('/Users/vborovic/workspace/DS/pronunciation-text/*.txt')]
#
# subfolders = ['2_lines', 'many_lines']
# for f in fls:
#     subfolder = subfolders[len(open(f).readlines()) > 2]
#     new_path = os.path.join(os.path.dirname(f), subfolder, os.path.basename(f))
#     print(new_path)
#     shutil.move(f, new_path)


def get_chapters():
    path = "/Users/vborovic/Google Drive/English/Pronunciation/Self_Study/English phonetics and pronunciation practice/"
    files = glob.glob(f'{path}*/*.mp3')
    names = [os.path.splitext(os.path.basename(f))[0] for f in files]
    df = pd.DataFrame(data=[[n] + list(map(int, n.split('.'))) for n in names], columns='value,ch1,ch2,ch3'.split(','))
    df = df.sort_values(by='ch1,ch2,ch3'.split(',')).reset_index(drop=True)
    return df


def get_lines():
    with open('/Users/vborovic/Desktop/pronunciation.txt') as f:
        text = f.read()
    return list(map(str.strip, text.splitlines()))


def line_index(lines: list, value: str, ):
    line: str
    for i, line in enumerate(lines):
        if line.startswith(value):
            return i


def split_text():
    df = get_chapters()
    lines = get_lines()
    for i, row in df.iterrows():
        try:
            next_row = df.iloc[i + 1]
            next_value = next_row['value']
        except IndexError:
            next_value = None
        position = line_index(lines, row['value'])
        if next_value:
            next_position = line_index(lines, next_value)
            selected_lines = lines[position:next_position]
        else:
            selected_lines = lines[position:]

        for i, l in enumerate(selected_lines):
            if l.startswith('Chapter') or l.startswith(f'{row["ch1"]}.{row["ch2"] + 1}'):
                selected_lines = selected_lines[:i]
                break

        with open(f'/Users/vborovic/workspace/DS/pronunciation-text/{row["value"]}.txt', 'w') as fout:
            fout.write('\n'.join(selected_lines))


def sort_numericly(s):
    chapter = os.path.splitext(os.path.basename(s))[0]
    l = list(map(int, chapter.split('.')))
    return l + [0, 0, 0][len(l):]


def get_single_line_words_csv():
    fls = sorted([f for f in glob.glob('/Users/vborovic/workspace/DS/pronunciation-text/2_lines/*.txt')],
                 key=sort_numericly)
    result = []
    for f in fls:
        chapter = os.path.splitext(os.path.basename(f))[0]
        first, second = open(f).read().splitlines()
        parts = re.split('[,;/]', second)
        for i, part in enumerate(parts):
            result.append(sort_numericly(f) + [chapter, part.strip(), i])

    df = pd.DataFrame(data=result, columns='ch1,ch2,ch3,chapter,word,order'.split(','))
    df.to_csv('single_line_words.csv', index=False)


def top_3000_oxford():
    levels = ['A1', 'A2', 'B1', 'B2']
    words = open('/Users/vborovic/Downloads/The Oxford 3000TM by CEFR level.txt').read().splitlines()
    level = None
    result = []
    for w in words:
        if w in levels:
            level = w
        else:
            result.append(list(w.split(' ', 1)) + [level])

    df = pd.DataFrame(data=result, columns='word,comment,level'.split(',')).drop_duplicates(subset=['word'])
    df.to_csv('top_3000_oxford.csv')


def join_oxford_and_line_words():
    df = pd.read_csv('single_line_words_v2.csv')
    words_3000_df = pd.read_csv('top_3000_oxford_v2.csv')

    pronunciation_to_oxford_level = []
    for _, row in df.iterrows():
        words = row.word.split()
        pronunciation_id = row.id
        level_ids = list(words_3000_df[words_3000_df.word.isin(words)].id)
        pronunciation_to_oxford_level += list(zip([pronunciation_id] * len(level_ids), level_ids))

    df_pronunciation_to_oxford_level = pd.DataFrame(data=pronunciation_to_oxford_level,
                                                    columns=['pronunciation_id', 'oxford_id'])
    df_pronunciation_to_oxford_level.to_csv('pronunciation_to_oxford_level.csv', index=False)
