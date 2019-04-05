from pytest import mark, raises

from wedding_planner import GuestList, Table


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


@mark.parmetrize('invalid_number', [0, 6])
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
