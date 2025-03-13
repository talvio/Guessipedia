import pytest
from coordinates import convert_lat_lon_to_float, which_is_north, which_is_east, get_currant_location, compare_distance
from unittest.mock import patch


test_data_pos_conversion = [
    (10, 10, (10,10)),
    (-10, 10, (-10,10)),
    ("10S", "10E", (-10, 10)),
    ("10.0N", "10.0W", (10, -10)),
    ("10.0N", "-10.0W", (None, None)),
    ("181.0N", "180.0W", (None, None)),
]

test_data_which_is_north = [
    ((10, 10), (10, 10), 0),
    ((-10, 10), (10, 10), 2),
    ((80, 10), (-90, 10), 1),
    ((180, 10), (0, 10), None),
    ((0, 10), ("1S", 10), 1),
    ((181, 10), (0,10), None),
]

test_data_which_is_east = [
    ((10, 10), (10, 10), 0),
    ((-10, 100), (10,10), 1),
    ((18, "10E"), (0, "10W"), 1),
    ((18, -10), (0, -12), 1),
    ((18, "10W"), (0, "12W"), 1),
]

@pytest.mark.parametrize("lat, lon, pos_in_float", test_data_pos_conversion)
def test_convert_lat_lon_to_float(lat, lon, pos_in_float):
    assert convert_lat_lon_to_float((lat, lon)) == pos_in_float

@pytest.mark.parametrize("pos1, pos2, first_or_second", test_data_which_is_north)
def test_which_is_north(pos1, pos2, first_or_second):
    assert which_is_north(pos1, pos2) == first_or_second

@pytest.mark.parametrize("pos1, pos2, first_or_second", test_data_which_is_east)
def test_which_is_east(pos1, pos2, first_or_second):
    assert which_is_east(pos1, pos2) == first_or_second

def test_get_currant_location(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'Turku')
    lat, lon = get_currant_location(0)
    assert int(lat) == 60
    assert int(lon) == 22
    monkeypatch.setattr('builtins.input', lambda _: 'Canary islands')
    lat, lon = get_currant_location(0)
    assert int(lat) == 28
    assert int(lon) == -16

test_data_compare_distance = [
    ((0, 0), (0, 0), (10, 10), 1),
    ((0, 0), (0, 0), (0, 0), 0),
    ((0, 0), (60, -60), (60, 60), 0),
    ((60, 20), (60, -60), (60, 60), 2),
]
@pytest.mark.parametrize("my_location, loc1, loc2, first_or_second", test_data_compare_distance)
def test_compare_distance(my_location, loc1, loc2, first_or_second):
    assert compare_distance(my_location, loc1, loc2) == first_or_second
