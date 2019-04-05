from pytest import raises

from wedding_planner import Table, TableFull


def test_has_given_capacity():
    table = Table(5)
    assert table.capacity == 5


def test_new_table_is_empty():
    table = Table(5)
    assert len(table._guests) == 0


def test_element_contained_in_the_table():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam', 'Jill'])
    assert 'Sam' in table


def test_element_not_contained_in_the_table():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam', 'Jill'])
    assert 'Rumplestilskin' not in table


def test_table_is_iterable():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam', 'Jill'])
    result = [e for e in table]
    assert sorted(result) == ['Donna', 'Jeff', 'Jill', 'Sam']


def test_string_representation_returns_ordered_set_representation():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam', 'Jill'])
    result = str(table)
    assert result == '{Donna; Jeff; Jill; Sam}'


def test_occupied_seats_returns_number_of_people_at_table():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam'])
    assert table.occupied_seats == 3


def test_no_seats_occupied_at_table_returns_0():
    table = Table(5)
    assert table.occupied_seats == 0


def test_full_table_returns_0_empty_seats():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam', 'Jill', 'Todd'])
    assert table.empty_seats == 0


def test_no_occupied_seats_returns_capacity_for_empty_seats():
    table = Table(3)
    assert table.empty_seats == 3


def test_empty_seats_returns_non_occupied_seats_till_full_table():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam'])
    assert table.empty_seats == 2


def test_adding_guest_to_empty_table():
    table = Table(5)
    table.add('Sarah')
    assert table._guests == {'Sarah'}


def test_adding_guest_to_full_table_raises_error():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam', 'Jill', 'Todd'])
    with raises(TableFull):
        table.add('Jim')


def test_adding_guest_to_partially_occupied_table():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna'])
    table.add('Sarah')
    assert 'Sarah' in table._guests


def test_removing_guest_from_table_vacates_seat():
    table = Table(5)
    table._guests = set(['Jeff', 'Donna', 'Sam'])
    table.remove('Jeff')
    assert table._guests == {'Donna', 'Sam'}


def test_removing_non_existing_guest_does_not_raise_error():
    table = Table(5)
    table._guests = set(['Donna', 'Sam'])
    table.remove('Jeff')
    assert table._guests == {'Donna', 'Sam'}


def test_removing_guest_from_empty_table_does_not_raise_error():
    table = Table(5)
    table.remove('Jeff')
    assert len(table._guests) == 0
