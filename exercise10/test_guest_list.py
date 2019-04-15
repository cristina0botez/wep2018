from pytest import mark, raises

from wedding_planner import GuestList, Table, Person, NotRegistered


def test_guest_list_creates_empty_table_list():
    gl = GuestList(5, 10)
    assert len(gl._tables) == 0
    assert len(gl._unassigned) == 0


def test_guest_list_created_with_number_of_tables():
    gl = GuestList(5, 10)
    assert gl._number_of_tables == 5


def test_guest_list_passes_on_table_size_to_table():
    gl = GuestList(5, 10)
    assert gl._tables[0].capacity == 10


def test_length_of_empty_guest_list_returns_0():
    gl = GuestList(5, 10)
    assert len(gl) == 0


def test_length_of_guest_list_includes_seated_and_unassigned_guests():
    gl = GuestList(5, 10)
    gl._tables[0].add('Banica')
    gl._tables[1].add('Ionica')
    gl._tables[1].add('Sarah')
    gl._tables[5].add('Dan')
    gl._unassigned.add('Kanye')
    gl._unassigned.add('Jay-Z')
    assert len(gl) == 6


def test_string_representation_returns_formatted_string_with_ordered_tables_and_guests():  # noqa
    gl = GuestList(5, 10)
    gl._tables[0].add('Banica')
    gl._tables[1].add('Sarah')
    gl._tables[1].add('Ionica')
    gl._tables[1].add('Florentin')
    gl._tables[4].add('Dan')
    gl._tables[4].add('Sorin')
    gl._unassigned.add('Kanye')
    gl._unassigned.add('Jay-Z')
    expected = ('0\n\tBanica\n1\n\tFlorentin\n\tIonica\n\tSarah\n4\n\tDan\n'
                '\tSorin\n')
    assert str(gl) == expected


def test_empty_table_does_not_appear_in_list():
    gl = GuestList(5, 10)
    gl._tables[1] = Table(10)
    assert str(gl) == ''


def test_no_string_representation_for_unassigned_guests():
    gl = GuestList(5, 10)
    gl._unassigned.add('Kanye')
    gl._unassigned.add('Jay-Z')
    assert str(gl) == ''


@mark.parametrize('invalid_number', [0, 6])
def test_assigning_guest_to_invalid_table_number_raises_error(invalid_number):
    gl = GuestList(5, 10)
    with raises(ValueError):
        gl.assign('You', invalid_number)


def test_assign_guest_to_table():
    gl = GuestList(5, 10)
    gl.assign('Ann', 3)
    assert 'Ann' in gl._tables[3]


def test_reassigning_guest_changes_table_number():
    gl = GuestList(5, 10)
    gl._tables[3].add('Ann')
    gl.assign('Ann', 1)
    assert 'Ann' not in gl._tables[3]
    assert 'Ann' in gl._tables[1]


def test_assigning_new_guest_to_none_table_sets_them_as_unassigned():
    gl = GuestList(5, 10)
    gl.assign('Ann', None)
    assert 'Ann' in gl._unassigned
    assert len(gl._tables) == 0


def test_reassigning_guest_to_none_moves_guest_to_unassigned_list():
    gl = GuestList(5, 10)
    gl._tables[3].add('Ann')
    gl.assign('Ann', None)
    assert 'Ann' in gl._unassigned
    assert len(gl._tables) == 1
    assert gl._tables[3].occupied_seats == 0


def test_empty_table_returns_no_guests():
    gl = GuestList(5, 10)
    result = gl.table(1)
    assert result == []


def test_table_with_guests_returns_them_in_a_list_in_ascending_ordered():
    gl = GuestList(5, 10)
    gl._tables[1].add('Sam')
    gl._tables[1].add('Ann')
    gl._tables[1].add('Phill')
    gl._tables[1].add('Sarah')
    gl._tables[1].add('Bill')
    result = gl.table(1)
    assert result == ['Ann', 'Bill', 'Phill', 'Sam', 'Sarah']


def test_unassigned_returns_list_of_guests_assigned_to_none():
    gl = GuestList(5, 10)
    gl.assign('Beth', None)
    gl.assign('Vanessa', None)
    gl.assign('Anna', None)
    result = gl.unassigned()
    assert result == ['Anna', 'Beth', 'Vanessa']


def test_find_table_for_returns_first_found_table_number_for_guest():
    gl = GuestList(10, 2)
    gl._tables[2].add('Annabella')
    gl._tables[4].add('Ann')
    gl._tables[7].add('Ann')
    result = gl.find_table_for('Ann')
    assert result == 4


def test_table_number_for_unassigned_guest_is_none():
    gl = GuestList(10, 2)
    gl._unassigned.add('Ann')
    result = gl.find_table_for('Ann')
    assert result is None


def test_unregistered_guest_raises_error():
    gl = GuestList(10, 2)
    with raises(NotRegistered):
        gl.find_table_for('Ann')


def test_free_space_returned_for_all_tables_in_empty_guest_list():
    gl = GuestList(3, 7)
    result = gl.free_space()
    assert result == {1: 7, 2: 7, 3: 7}


def test_free_space_returns_0_when_all_tables_occupied():
    gl = GuestList(2, 2)
    gl._tables[1].add('Ann')
    gl._tables[1].add('Bill')
    gl._tables[2].add('Dan')
    gl._tables[2].add('Paul')
    result = gl.free_space()
    assert result == {1: 0, 2: 0}


def test_free_space_returned_for_each_table():
    gl = GuestList(4, 3)
    gl._tables[1].add('Ann')
    gl._tables[1].add('Bill')
    gl._tables[3].add('Dan')
    gl._tables[3].add('Paul')
    gl._tables[3].add('Fran')
    gl._tables[4].add('Phill')
    result = gl.free_space()
    assert result == {1: 1, 2: 3, 3: 0, 4: 2}


def test_guests_empty_for_empty_guest_list():
    gl = GuestList(2, 2)
    result = gl.guests()
    assert result == []


def test_unassigned_guests_not_listed():
    gl = GuestList(2, 2)
    gl._unassigned.add('Ann')
    result = gl.guests()
    assert result == []


def test_guests_returns_guest_list_ordered_by_table_number_last_and_first_names():  # noqa
    gl = GuestList(3, 4)
    gl._tables[3].add(Person('Gena', 'Frank'))
    gl._tables[1].add(Person('Zack', 'Paulson'))
    gl._tables[4].add(Person('Andrew', 'Andrews'))
    gl._tables[3].add(Person('Samantha', 'Andrews'))
    gl._tables[1].add(Person('Gena', 'Paulson'))
    gl._tables[3].add(Person('Paula', 'Bayleys'))
    result = gl.guests()
    expected = [Person('Gena', 'Paulson'),
                Person('Zack', 'Paulson'),
                Person('Samantha', 'Andrews'),
                Person('Paula', 'Bayleys'),
                Person('Gena', 'Frank'),
                Person('Andrew', 'Andrews')]
    assert result == expected
