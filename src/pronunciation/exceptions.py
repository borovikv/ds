import glob
import re

import pandas as pd

p = re.compile(r'([.,?!])')


def get_files():
    return sorted(glob.glob(f'words/pronunciation-text/exceptions/*.txt'))


def split_join(tail):
    names = [tail[r] for r in range(len(tail)) if r % 2 == 0]
    texts = [tail[r] for r in range(len(tail)) if r % 2 == 1]
    return names, texts


result = []
for f in get_files():
    with open(f) as fin:
        lines = fin.read().splitlines()

    header, *tail = lines
    chapter, name = header.split(maxsplit=1)
    names, texts = split_join(tail)
    names = [n.split(')', maxsplit=1)[1].strip() for n in names]
    texts = [list(map(lambda s: s.strip(' ,.'), p.split(r))) for r in texts]
    texts = [[''.join(p) for p in zip(*split_join(row))] for row in texts]
    print(chapter, len(texts), sum(len(r) for r in texts))
    i = 0
    for _type, _texts in zip(names, texts):
        for text in _texts:
            result.append(dict(
                text=text,
                type=_type,
                chapter=chapter,
                chapter_name=name,
                order=i
            ))
            i += 1

df = pd.DataFrame(result)
df.to_csv('words/exceptions.csv', index=False)
