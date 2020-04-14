from pprint import pprint

import preparation.graphs.tasks as subj


def test_find_path():
    """
         a
       /   \
       b - c
       \  /
        d
    """
    a, b, c, d = 'abcd'
    g = {
        a:[b, c],
        b:[c, d],
        c:[d]
    }
    result = subj.find_path_breadth(g, a, d)
    assert result == [[a, b, d], [a, c, d]]

    result = subj.find_path_depth(g, a, d)
    pprint(result)
