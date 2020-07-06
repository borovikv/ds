import re
from collections import Counter


def count_words():
    text = get_text('Pelham.txt')
    c = Counter(filter(bool, re.split(r'[^a-z0-9_]', text.lower())))

    print('unique words', len(c))
    print('total words', sum(c.values()))

    prepositions = get_prepositions()
    main_words = ([k, v] for k, v in c.items() if k not in prepositions + ['a', 'the'])
    words = sorted(main_words, key=lambda p: list(reversed(p)), reverse=True)
    for w, t in words:
        if t < 10:
            break
        print(f'{w}\t{t}')

    for a in ['a', 'the']:
        print(f'{a}: {c.get(a)}')


def count_prepositions(text):
    result = {p: len(re.findall(r'\b{}\b'.format(p), text.lower())) for p in (get_prepositions())}
    for k, v in sorted(result.items(), key=lambda p: list(reversed(p)), reverse=True):
        print(f'{k}\t{v}')


def get_text(name):
    with open(f'/Users/vborovic/workspace/DS/data/prepositions/{name}') as f:
        return f.read()


def get_prepositions():
    with open('/Users/vborovic/workspace/DS/data/prepositions') as f:
        return list(filter(bool, map(str.strip, f.readlines())))

# count_words()
# count_prepositions(text)
