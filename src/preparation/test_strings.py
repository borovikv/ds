import pytest

import preparation.strings as subj


def test_contains_not_unique_symbols():
    assert subj.contains_not_unique_symbols('aabc') is False
    assert subj.contains_not_unique_symbols('abcd') is True


def test_contains_not_unique_symbols_2():
    assert subj.contains_not_unique_symbols_2('abcc') is False
    assert subj.contains_not_unique_symbols_2('abcd') is True
    assert subj.contains_not_unique_symbols_2('heloward') is True


def test_is_permutation():
    assert subj.is_permutation('abc', 'cba') is True
    assert subj.is_permutation('abc', 'cbd') is False


def test_is_permutation_2():
    assert subj.is_permutation_2('abc', 'cba') is True
    assert subj.is_permutation_2('abc', 'cbd') is False
    assert subj.is_permutation_2('aac', 'aad') is False


def test_permutations():
    result = subj.permutation('abc')
    assert list(sorted(result)) == list(sorted('abc bac bca cba cab acb'.split()))


@pytest.mark.parametrize('a,b,expected', [
    ('pale', 'bale', True),
    ('pales', 'pale', True),
    ('pale', 'ple', True),
    ('pale', 'bake', False),
    ('pales', 'pal', False),
])
def test_is_one_simbol_behind(a, b, expected):
    assert subj.is_one_simbol_behind_1_5(a, b) is expected


@pytest.mark.parametrize('input,expected', [
    ('aabcccccaaa', 'a2b1c5a3'),
    # ('abcd', 'abcd'),
])
def test_compress_string(input, expected):
    result = subj.compress_string(input)
    assert expected == result

    result = subj.compress_string_2(input)
    assert expected == result


def test_1_8():
    matrix = [
        [0, 2, 3],
        [1, 0, 3],
        [1, 2, 3],
    ]
    result = subj.set_0(matrix)
    expected = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 3],
    ]
    assert expected == result

