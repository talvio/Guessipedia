"""
def test_get_random_page_with_coordinates():
    pages = get_random_page_with_coordinates()
    assert isinstance(pages[0][0], str) is True
    assert isinstance(pages[1][0], str) is True
    lat, lon = pages[0][1], pages[0][2]
    assert convert_lat_lon_to_float((lat, lon)) == (lat, lon)
    lat, lon = pages[1][1], pages[1][2]
    assert convert_lat_lon_to_float((lat, lon)) == (lat, lon)

"""