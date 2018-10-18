import pytest
from myrange import myrange2, myrange3


def test_myrange2_is_a_list():
    output = myrange2(10)
    assert type(output) is list


@pytest.mark.parametrize('first, second, third, output', [
    (10, None, None, list(range(10))),
    (10, 20, None, list(range(10, 20))),
    (20, 10, None, []),
    (10, 20, 2, list(range(10, 20, 2))),
    (10, 20, 3, list(range(10, 20, 3))),
    (0, -7, -1, list(range(0, -7, -1))),
    (9, 2, -3, list(range(9, 2, -3)))
])
def test_myrange2(first, second, third, output):
    if third:
        assert myrange2(first, second, third) == output
    elif second:
        assert myrange2(first, second) == output
    else:
        assert myrange2(first) == output


def test_myrange2_raises_error_for_step_0():
    with pytest.raises(ValueError):
        myrange2(1, 2, 0)


def test_myrange3_is_a_generator():
    output = myrange3(10)
    assert iter(output) is output


@pytest.mark.parametrize('first, second, third, output', [
    (10, None, None, list(range(10))),
    (10, 20, None, list(range(10, 20))),
    (20, 10, None, []),
    (10, 20, 2, list(range(10, 20, 2))),
    (10, 20, 3, list(range(10, 20, 3))),
    (0, -7, -1, list(range(0, -7, -1))),
    (9, 2, -3, list(range(9, 2, -3)))
])
def test_myrange3(first, second, third, output):
    if third:
        assert list(myrange3(first, second, third)) == output
    elif second:
        assert list(myrange3(first, second)) == output
    else:
        assert list(myrange3(first)) == output


def test_myrange3_raises_error_for_step_0():
    with pytest.raises(ValueError):
        list(myrange3(1, 2, 0))
