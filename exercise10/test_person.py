from pytest import raises

from wedding_planner import Person


def test_person_first_and_last_names_are_mandatory():
    with raises(TypeError):
        Person()
    with raises(TypeError):
        Person(first='A')
    with raises(TypeError):
        Person(last='A')
    Person('A', 'B')


def test_person_has_first_and_last_names():
    p = Person('John', 'Doe')
    assert p.first == 'John'
    assert p.last == 'Doe'


def test_persons_with_same_name_are_equal():
    p1 = Person('John', 'Doe')
    p2 = Person('John', 'Doe')
    assert p1 is not p2 and p1 == p2


def test_2_persons_compared_by_last_name_ascending():
    p1 = Person('Adam', 'Smith')
    p2 = Person('John', 'Doe')
    assert p1 > p2 and p2 < p1


def test_2_persons_with_same_last_name_compared_by_first():
    p1 = Person('John', 'Doe')
    p2 = Person('Jane', 'Doe')
    assert p1 > p2 and p2 < p1


def test_person_displayed_by_last_and_first_name():
    p = Person('John', 'Doe')
    assert str(p) == 'Doe, John'
