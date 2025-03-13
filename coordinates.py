"""
Provide functions for geographic calculations.

This module includes functions for processing latitude and longitude,
comparing distances between coordinates, and determining whether one
location is further north or east than another. It also allows users
to retrieve their current location based on an inputted address.
"""

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from colors import *


def convert_lat_lon_to_float(pos):
    """
    Convert latitude and longitude values into floats.

    Args:
        pos (tuple): A tuple containing latitude and longitude as either floats
                     or strings that can be converted into floats.
                     - Latitude should be between -90 and 90.
                     - Longitude should be between -180 and 180.
                     - 'N' or 'S' can be used at the end of latitude, but not with a minus sign.
                     - 'E' or 'W' can be used at the end of longitude, but not with a minus sign.

    Returns:
        tuple: A tuple containing (latitude, longitude) as floats. Returns (None, None) if input is invalid.
    """
    lat, lon = str(pos[0]), str(pos[1])
    if lat[-1] == 'S':
        lat = "-" + lat[:-1]
    if lat[-1] == 'N':
        lat = lat[:-1]
    if lon[-1] == 'W':
        lon = "-" + lon[:-1]
    if lon[-1] == 'E':
        lon = lon[:-1]
    try:
        pos_latitude = float(lat)
        pos_longitude = float(lon)
    except ValueError:
        return None, None
    if pos_latitude < -90 or pos_latitude > 90 or pos_longitude < -180 or pos_longitude > 180:
        return None, None
    return pos_latitude, pos_longitude


def which_is_north(pos1, pos2):
    """
    Determine which of two coordinates is further north.

    Args:
        pos1 (tuple): A tuple containing latitude and longitude.
        pos2 (tuple): A tuple containing latitude and longitude.

    Returns:
        int:
            - 1 if the first location is further north.
            - 2 if the second location is further north.
            - 0 if they are equally north.
            - None if input is invalid.
    """
    pos1_latitude, pos1_longitude = convert_lat_lon_to_float(pos1)
    pos2_latitude, pos2_longitude = convert_lat_lon_to_float(pos2)
    if pos1_latitude is None or pos2_latitude is None or pos1_longitude is None or pos2_longitude is None:
        return None
    if pos1_latitude == pos2_latitude:
        return 0
    if pos1_latitude > pos2_latitude:
        return 1
    return 2


def which_is_east(pos1, pos2):
    """
    Determine which of two coordinates is further east.

    Args:
        pos1 (tuple): A tuple containing latitude and longitude.
        pos2 (tuple): A tuple containing latitude and longitude.

    Returns:
        int:
            - 1 if the first location is further east.
            - 2 if the second location is further east.
            - 0 if they are equally east.
            - None if input is invalid.
    """
    pos1_latitude, pos1_longitude = convert_lat_lon_to_float(pos1)
    pos2_latitude, pos2_longitude = convert_lat_lon_to_float(pos2)
    if pos1_latitude is None or pos2_latitude is None or pos1_longitude is None or pos2_longitude is None:
        return None
    if pos1_longitude == pos2_longitude:
        return 0
    if pos1_longitude > pos2_longitude:
        return 1
    return 2


def compare_distance(my_location, loc1, loc2):
    """
    Compare distances of two locations from a reference location.

    Args:
        my_location (tuple): The reference location (latitude, longitude).
        loc1 (tuple): The first location to compare.
        loc2 (tuple): The second location to compare.

    Returns:
        tuple:
            - (1, distance1, distance2) if loc1 is closer.
            - (2, distance1, distance2) if loc2 is closer.
            - 0 if both distances are equal.
    """
    player_location = convert_lat_lon_to_float(my_location)
    location_1 = convert_lat_lon_to_float(loc1)
    location_2 = convert_lat_lon_to_float(loc2)

    distance1 = geodesic(player_location, location_1).kilometers
    distance2 = geodesic(player_location, location_2).kilometers

    if distance1 == distance2:
        return 0
    return (1, distance1, distance2) if distance1 < distance2 else (2, distance1, distance2)


def distance_pos1_pos2(pos1, pos2):
    """
    Calculate the geodesic distance between two positions.

    Args:
        pos1 (tuple): The first location (latitude, longitude).
        pos2 (tuple): The second location (latitude, longitude).

    Returns:
        float: The distance between the two locations in kilometers, rounded to the nearest whole number.
    """
    location_1 = convert_lat_lon_to_float(pos1)
    location_2 = convert_lat_lon_to_float(pos2)
    distance = geodesic(location_1, location_2).kilometers
    return round(distance)


def get_current_location(player):
    """
    Prompt the user to enter their location and retrieve latitude and longitude.

    The function uses the Nominatim geocoder to convert the input address
    into geographic coordinates.

    Args:
        player (str): The name of the player.

    Returns:
        tuple: A tuple containing (latitude, longitude) of the entered location.

    Note:
        - The user can enter a country, major city, or street address.
        - If the location is invalid, the user is prompted to try again.
    """
    while True:
        address = input(f"{BRIGHT_YELLOW}{player}{RESET_STYLE}{BRIGHT_MAGENTA} enter your location: {RESET_STYLE}")
        geolocator = Nominatim(user_agent='guessipedia')
        location = geolocator.geocode(address)
        """
        check the location exists
        """
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            print(f"{BRIGHT_RED}Couldn't find your location {RESET_STYLE}{GREEN}{address},{RESET_STYLE}{BRIGHT_RED} please try again.{RESET_STYLE}")


def pos_to_txt(pos):
    lat = f"{-float(pos[0]):.2f}°S" if pos[0] < 0 else f"{float(pos[0]):.2f}°N"
    lon = f"{-float(pos[1]):.2f}°W" if pos[1] < 0 else f"{float(pos[1]):.2f}°E"
    return f"{lat} {lon}"
