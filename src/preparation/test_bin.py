import preparation.binary_ariphmentics as subj


def test_insert():
    m = int('10011', 2)
    n = int('10000000000', 2)
    i = 2
    j = 6
    result = subj.insert(m, n, i, j)
    expected = int('10001001100', 2)
    print('result', f'{result:b}')
    assert expected == result


def test_print_binary():
    result = subj.print_binary(0.72)
    print(result)
