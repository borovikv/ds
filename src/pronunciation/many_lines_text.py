import glob
import re

import pandas as pd


def get_files(folder):
    return glob.glob(f'words/pronunciation-text/{folder}/*.txt')


def parse_many_lines():
    files = get_files(folder='many_lines')
    result = []
    for f in files:
        text = open(f).read()
        header, *lines = text.splitlines()
        chapter, name = header.split(maxsplit=1)
        sub_headers = [line for line in lines if re.match(r'^[a-z]\) ', line)]
        texts = [line for line in lines if not re.match(r'^[a-z]\) ', line)]
        row = dict(chapter=chapter, chapter_name=name)
        c = 0
        for s, t in zip(sub_headers, texts):
            _, a_type = s.split(maxsplit=1)
            for t1 in t.split(','):
                result.append(dict(row, order=c, text=t1.strip(), type=a_type.strip()))
                c += 1

    df = pd.DataFrame(result)
    df.sort_values('chapter').to_csv('words/many_lines.csv', index=False)


# parse_many_lines()


def parse_sentences():
    files = get_files('s')
    result = []

    for f in files:
        text = open(f).read()
        header, *lines = text.splitlines()
        chapter, *_ = header.split()
        row = dict(chapter=chapter)
        if 'Dialogue' in header:
            for i, l in enumerate(lines):
                _, text = re.split(r'^[A-Z]:', l)
                result.append(dict(row, order=i, text=text.strip(), type='Dialogue'))
        elif 'Sentence' in header:
            for i, l in enumerate(lines):
                _, text = re.split(r'^\d+ ', l)
                result.append(dict(row, order=i, text=text.strip(), type='Sentence'))
        else:
            raise Exception()

    df = pd.DataFrame(result)
    df.to_csv('words/sentences.csv', index=False)


def parse_wfs():
    files = get_files('wfs')
    result = []

    for f in files:
        text = open(f).read()
        header, *lines = text.splitlines()
        chapter, name = header.split(maxsplit=1)
        row = dict(chapter=chapter, chapter_name=name.strip())
        # lines[0] Words
        # lines[2] Phrases
        # lines[4] Sentences
        c = 0
        for t in map(str.strip, lines[1].split(',')):
            result.append(dict(row, order=c, text=t.strip(), type='Word'))
            c += 1

        for t in map(str.strip, lines[3].split(',')):
            result.append(dict(row, order=c, text=t.strip(), type='Phrase'))
            c += 1

        for l in lines[5:]:
            _, text = re.split(r'^\d+ ', l)
            result.append(dict(row, order=c, text=text.strip(), type='Sentence'))
            c += 1

    df = pd.DataFrame(result)
    df.to_csv('words/wfs.csv', index=False)

# parse_wfs()
