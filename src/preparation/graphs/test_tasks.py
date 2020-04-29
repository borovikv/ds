from pprint import pprint

import preparation.graphs.tasks as subj


def test_find_path():
    a, b, c, d, e = 'abcde'

    r"""
         a
       /   \
       b - c
       \  /
        d
        |
        e
    """
    g = {
        a: [b, c],
        b: [c, d],
        c: [d],
        d: [e]
    }
    result = subj.find_path_breadth(g, start=a, end=e)
    # assert result == [[a, b, d, e], [a, c, d, e]]
    pprint(result)

    # result = subj.find_path_depth(g, a, e)
    # pprint(result)
