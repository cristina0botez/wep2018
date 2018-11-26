from interzip import interzip


def test_returns_iterator():
    m = interzip('abc', 'def')
    assert m == iter(m)


def test_simple():
    m = interzip('abc', 'def')
    assert list(m) == list('adbecf')


def test_not_same_length():
    m = interzip('abc', 'de')
    assert list(m) == list('adbe')
