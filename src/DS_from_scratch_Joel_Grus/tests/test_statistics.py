import DS_from_scratch_Joel_Grus.statistics as subject


def test_median_when_vector_has_odd_length():
    assert subject.median([1, 2, 100]) == 2


def test_median_when_vector_has_even_length():
    assert subject.median([-1000, 2, 100, 10e6]) == (2 + 100) / 2


def test_quantile():
    # when vector is odd
    v = [-1000, 2, 100, 10e3, 10e6, ]
    assert subject.quantile(v, 0.5) == subject.median(v)

    # when vector is even
    v = [-1000, 2, 100, 10e3]
    quantile = subject.quantile(v, 0.5)
    assert quantile == 100
    assert quantile != subject.median(v)

    v = [-1000, 2, 100, 10e3, 10e6, ]
    assert subject.quantile(v, 0.75) == 10e3
