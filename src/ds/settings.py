import os


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RESOURCE_ROOT = os.path.join(BASE_PATH, 'resources')


def path(ch: str, *args: str):
    return os.path.join(RESOURCE_ROOT, 'pydata-book-master', f'ch{ch}', *args)
