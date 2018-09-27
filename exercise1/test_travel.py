from collections import defaultdict
from io import StringIO

from pytest import mark, raises

from travel import (
    extract_state_and_city, store_visit, collect_places, display_places,
    visits, InputFinished
)


@mark.parametrize('user_input', ('New York, USA',
                                 ' New York,USA ',
                                 'New York ,USA'))
def test_extract_from_input_returns_state_and_city(user_input):
    result = extract_state_and_city(user_input)
    assert result == ('USA', 'New York')


@mark.parametrize('invalid_input', ('New York',
                                    ', USA',
                                    'New York,',
                                    ',,'))
def test_invalid_input_raises_value_error(invalid_input):
    with raises(ValueError):
        extract_state_and_city(invalid_input)


def test_empty_input_raises_input_finished():
    with raises(InputFinished):
        extract_state_and_city('')


def test_first_visit_stored_in_dictionary():
    d = defaultdict(dict)
    store_visit('USA', 'New York', d)
    assert d == {'USA': {'New York': 1}}


def test_third_visit_stored_in_dictionary():
    d = defaultdict(dict, [('USA', {'New York': 2})])
    store_visit('USA', 'New York', d)
    assert d == {'USA': {'New York': 3}}


def test_city_added_alonside_others_in_same_country():
    d = defaultdict(dict, [('USA', {'New York': 2})])
    store_visit('USA', 'Washington', d)
    assert d == {'USA': {'New York': 2, 'Washington': 1}}


def test_country_added_alonside_others():
    d = defaultdict(dict, [('USA', {'New York': 1})])
    store_visit('Italy', 'Florence', d)
    assert d == {'USA': {'New York': 1}, 'Italy': {'Florence': 1}}


EMPTY_PLACE_INPUTS = StringIO('\n')
ONE_PLACE_INPUT = StringIO('London, England\n\n')
MANY_PLACE_INPUTS = StringIO('''Shanghai, China
Beijing, China
Tel Aviv, Israel
Haifa, Israel
Madrid, Spain
Barcelona, Spain

''')


def test_no_places(monkeypatch):
    visits.clear()
    monkeypatch.setattr('sys.stdin', EMPTY_PLACE_INPUTS)
    collect_places()
    assert len(visits) == 0


def test_one_place(monkeypatch):
    visits.clear()
    monkeypatch.setattr('sys.stdin', ONE_PLACE_INPUT)
    collect_places()
    assert len(visits) == 1


def test_many_places(monkeypatch):
    visits.clear()
    monkeypatch.setattr('sys.stdin', MANY_PLACE_INPUTS)
    collect_places()
    assert len(visits) == 3


def test_invalid_input(monkeypatch, capsys):
    visits.clear()
    monkeypatch.setattr('sys.stdin', StringIO('abcd\n\n'))
    collect_places()
    captured_out, captured_err = capsys.readouterr()
    assert captured_out.strip().startswith(
        "Tell me where you went: That's not a legal city, country combination")
    assert captured_out.strip().endswith("Tell me where you went:")


def test_sorting_cities(monkeypatch, capsys):
    visits.clear()
    monkeypatch.setattr('sys.stdin', StringIO('Shanghai, China\nBeijing, China'
                                              '\nBeijing, China\n\n'))
    collect_places()
    captured_out, captured_err = capsys.readouterr()

    display_places()
    captured_out, captured_err = capsys.readouterr()
    beijing_index = captured_out.index('Beijing')
    shanghai_index = captured_out.index('Shanghai')
    assert beijing_index < shanghai_index


def test_sorting_countries(monkeypatch, capsys):
    visits.clear()
    monkeypatch.setattr('sys.stdin', StringIO('Haifa, Israel\nLondon, England'
                                              '\nNew York, USA\n\n'))
    collect_places()
    captured_out, captured_err = capsys.readouterr()

    display_places()
    captured_out, captured_err = capsys.readouterr()
    israel_index = captured_out.index('Israel')
    england_index = captured_out.index('England')
    usa_index = captured_out.index('USA')
    assert england_index < israel_index
    assert israel_index < usa_index


def test_counting(monkeypatch, capsys):
    visits.clear()
    monkeypatch.setattr('sys.stdin', StringIO('Shanghai, China\nBeijing, China'
                                              '\nBeijing, China\n\n'))
    collect_places()
    captured_out, captured_err = capsys.readouterr()
    assert len(visits['China']) == 2

    display_places()
    captured_out, captured_err = capsys.readouterr()
    assert 'Beijing (2)' in captured_out
    assert 'Shanghai' in captured_out
