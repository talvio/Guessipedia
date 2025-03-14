"""
Retrieve Wikipedia page summaries and geolocation-based articles.

This module provides functions to fetch Wikipedia summaries,
search for articles based on latitude and longitude, and retrieve
random pages with coordinate data.
"""

import requests
import random
import sys

API_URL = "https://en.wikipedia.org/w/api.php"
CONNECTION_TIMEOUT = 3
READ_TIMOUT = 10


def shorten_text(max_sentences, text):
    """
    Shorten a longer text to a defined number of sentences.

    Args:
        max_sentences (int): The number of sentences to return.
        text (str): The text to be shortened.

    Returns:
        str: A shortened text containing the specified number of sentences.
    """
    if len(text.split(".")) <= max_sentences:
        return text
    return ".".join(text.split(".")[:max_sentences]) + "."


def access_wikimedia_api(params):
    """
    A fault tolerant way to access the Wikipedia API.
    :param params:
    :return: Tuple where the first value is True if the call was successful, False is not.
             The second is the result of the API call.
    """
    try:
        data = requests.get(API_URL, params=params, timeout=(CONNECTION_TIMEOUT, READ_TIMOUT)).json()
    except requests.exceptions.Timeout:
        return False, "(No description available. Access to wiki media timed out.)"
    except requests.exceptions.ConnectionError:
        return False, "(No description available. Access to wiki media failed.)"
    except requests.exceptions.HTTPError as err:
        return False, f"(No description available. Access to wiki media failed: {err}.)"
    except requests.exceptions.RequestException as err:
        return False, f"(No description available. Access to wiki media failed: {err}.)"
    return True, data


def get_extract(page_id=None, page_title=None, max_sentences=None):
    """
    Retrieve a short summary of a Wikipedia page.

    This function fetches the introductory extract from a Wikipedia page
    using either its page ID or title. The extract is limited to a specified
    number of sentences.

    Args:
        page_id (int, optional): The Wikipedia page ID.
        page_title (str, optional): The Wikipedia page title.
        max_sentences (int, optional): The maximum number of sentences to return.

    Returns:
        str: A summary of the Wikipedia page. Returns None if no page is found.
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True
    }
    if page_id is not None:
        params['pageids'] = page_id
    elif page_title is not None:
        params['titles'] = page_title
    else:
        return None

    great_success, data = access_wikimedia_api(params)
    if not great_success:
        return data
    page_id = list(data.get('query',{}).get('pages',{}).keys())[0]
    text_extract = data.get('query',{}).get('pages',{}).get(str(page_id), {}).get('extract', None)
    if max_sentences is not None:
        text_extract = shorten_text(max_sentences, text_extract)
    return text_extract


def find_page_ids_lat_lon(lat, lon, count=1):
    """
    Find Wikipedia pages based on geographic coordinates.

    This function searches for Wikipedia pages located within a
    10-kilometer radius of the given latitude and longitude.

    Args:
        lat (float): Latitude in decimal degrees (-90 to 90).
        lon (float): Longitude in decimal degrees (-180 to 180).
        count (int, optional): The number of pages to return. Default is 1.

    Returns:
        list: A list of tuples (page_id, title, lat, lon) for matching pages.
              Returns an empty list if no pages are found.
    """
    params = {
        "action": "query",
        "format": "json",
        "list": "geosearch",
        "gscoord": f"{lat}|{lon}",
        'gsradius': 10000,
        "gslimit": count
    }

    great_success, data = access_wikimedia_api(params)
    if not great_success:
        print(data)
        exit()

    return [(x.get('pageid'),x.get('title'),x.get('lat'),x.get('lon'))
            for x in data.get("query", {}).get('geosearch', [])]


def get_random_page_with_coordinates2(count=2):
    """
    Retrieve random Wikipedia articles that have geographic coordinates.

    This function selects random locations worldwide, searches for nearby
    Wikipedia articles, and ensures that the selected articles have
    latitude and longitude data.

    Args:
        count (int, optional): The number of random pages to retrieve. Default is 2.

    Returns:
        list: A list of tuples containing (page_title, latitude, longitude, page_id).
    """
    tries = 0
    step = 1
    random_pages = []
    while len(random_pages) < count:
        tries += step
        if tries > 5:
            step = -1
        if tries < 2:
            step = 1
        sys.stdout.write(f"\rFetching data: {' ':{1 if tries < 2 else 2}}"
                         f"{'[':<{tries}}*{']':>{6-tries+(tries//6)+(1 if tries < 2 else 0)}}                 ")
        sys.stdout.flush()
        lat = random.randint(-80, 80)
        lon = random.randint(-180, 180)
        random_page = find_page_ids_lat_lon(lat, lon, count=1)
        if len(random_page) == 0:
            continue
        page_id, title, lat, lon = random_page[0]
        random_pages.append((title, lat, lon, page_id))
    print()
    return random_pages


if __name__ == "__main__":
    """
    Demonstrate the module's functionality when run directly.

    This section retrieves random Wikipedia pages and their summaries,
    showcasing how the functions work.
    """
    pages = get_random_page_with_coordinates2(count=4)
    print("Random pages: ", pages)
    print(1, get_extract(pages[0][3], max_sentences=2))
    print(2, get_extract(pages[1][3], max_sentences=2))
