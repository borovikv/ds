import pytest

import preparation.p1.linked_list as subj


def test_find_dub():
    result = subj.remove_dub([1, 2, 1, 3, 2])
    assert result == [1, 2, 3]


def test_access():
    result = subj.access(list(range(10)), 7)
    assert 3 == result


@pytest.mark.parametrize('a,b,expected', [
    ([1], [0, 1], [1, 1]),
    ([7], [2], [9]),
    ([7], [3], [0, 1]),
    ([1, 5], [2, 3], [3, 8]),
    ([1, 5], [9, 5], [0, 1, 1]),
    ([7, 1, 6], [5, 9, 2], [2, 1, 9]),
    ([9, 9], [9, 9], [8, 9, 1]),
    ([9], [9, 9], [8, 0, 1]),
    ([9, 7, 8], [6, 8, 5], [5, 6, 4, 1]),
])
def test_sum_l(a, b, expected):
    result = subj.sum_l(a, b)
    assert expected == result


@pytest.mark.parametrize('a,b,expected', [
    ([7], [2], [9]),
    ([7], [3], [0, 1]),
    ([1, 5], [2, 3], [3, 8]),
    ([1, 5], [9, 5], [0, 1, 1]),
    ([7, 1, 6], [5, 9, 2], [2, 1, 9]),
    ([9, 9], [9, 9], [8, 9, 1]),
    ([9], [9, 9], [8, 0, 1]),
    ([9, 7, 8], [6, 8, 5], [5, 6, 4, 1]),
])
def test_sum_l_stright(a, b, expected):
    result = subj.sum_l_straight(r(a), r(b))
    print(r(a), r(b), r(expected))
    assert r(expected) == result


def r(l):
    return list(reversed(l))
