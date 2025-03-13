"""
Run the Guessipedia Challenge game.

This module implements a geography-based guessing game where players
compare locations in terms of distance, latitude (north), or longitude (east).
Players earn points for correct answers.
"""

import random
from ascii_map import print_location, print_locations

from coordinates import (
    which_is_north,
    which_is_east,
    compare_distance,
    get_current_location,
    distance_pos1_pos2,
    pos_to_txt,
)
from wiki_api import get_random_page_with_coordinates2, get_extract
from colors import *


def print_fancy_header():
    """
    Print the ASCII art header for the game.

    This function enhances the user experience by displaying
    a visually appealing title before the game starts.
    """
    header = f"""{YELLOW}
    ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
    ┃                                                                             ┃
    ┃ {RESET_STYLE}{BLUE}            🌍  G U E S S I P E D I A   C H A L L E N G E  🧭 {RESET_STYLE}{YELLOW}              ┃
    ┃                                                                             ┃
    ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
    {RESET_STYLE}"""
    print(header)


def introduce_game():
    """
    Introduce the game and explain the rules.

    This function prints a welcome message, explains the mechanics,
    and prepares the player for the challenge.
    """
    print_fancy_header()
    print(f"\n{BRIGHT_CYAN}                       🎉 Welcome to Guessipedia! 🎉")
    print("                        Test your geography skills!")
    print("For each correct guess, you earn points. Let's see how well you know the world! 🌎")
    print("\n      Type '1' or '2' to make your choice, or 'q' to quit at any time.")
    print(f"\n                         Ready? Let's go... 🚀{RESET_STYLE}\n")


def get_user_input(first_page_title, second_page_title):
    """
    Prompt the user to choose between two location options.

    Args:
        first_page_title (str): The title of the first location option.
        second_page_title (str): The title of the second location option.

    Returns:
        int: 1 if the first option is chosen, 2 if the second option is chosen.
    """
    while True:
        user_input = input(
            f"{BRIGHT_BLUE}1. {first_page_title}{RESET_STYLE}\n{BRIGHT_BLUE}"
            f"2. {second_page_title}\n{RESET_STYLE}{BRIGHT_MAGENTA}"
            f"Answer: {BRIGHT_BLUE}"
        )
        if user_input in ["1", "2"]:
            return int(user_input)
        print(f"{BRIGHT_RED}Invalid input. Please enter only 1 or 2.{RESET_STYLE}")


def get_number_of(element):
    """
    Get a numeric input from the user.

    Args:
        element (str): The item to be counted (e.g., "players", "rounds").

    Returns:
        int: The entered number.
    """
    while True:
        try:
            number_of = int(
                input(f"{BRIGHT_MAGENTA}Enter the number of {element}: {RESET_STYLE}")
            )
            return number_of
        except ValueError:
            print(f"{BRIGHT_RED}Invalid input the input must be a number! {RESET_STYLE}")


def get_player_data():
    """
    Get player name and location
    :return: player name and location
    """
    number_of_players = get_number_of('players')
    player_names = []
    player_locations = []
    for player in range(number_of_players):
        player_name = input(f"{BRIGHT_MAGENTA}\nPlayer {player + 1} enter your name: {RESET_STYLE}").capitalize()
        player_names.append(player_name)
        user_location = get_current_location(player_name)
        print_location(user_location, f"\n{BRIGHT_GREEN}You are here, {pos_to_txt(user_location)}!{RESET_STYLE}")
        player_locations.append(user_location)
    return player_names, player_locations


def ask_question_about_north(player, player_location, page_data):
    """
    Ask the user which of the two locations is more North.
    :param player: player name
    :param player_location: player location
    :param page_data: List of 2 tuples. The tuples contain the page data, title, position and wiki page_id
    :return: True if the player answer is correct, False otherwise.
    """
    first_page_title, first_latitude, first_longitude, first_page_id = page_data[0]
    second_page_title, second_latitude, second_longitude, second_page_id = page_data[1]

    print(f'\n{BRIGHT_YELLOW}{player} {RESET_STYLE}{BRIGHT_BLUE}'
          f'which location is further north?{RESET_STYLE}')

    player_answer = print_answer_options_and_get_answer(page_data, player_location)

    return player_answer == which_is_north((first_latitude, first_longitude),
                                       (second_latitude, second_longitude))


def ask_question_about_east(player, player_location, page_data):
    """
    Ask the user which of the two locations is more east.
    :param player: player name
    :param player_location: player location
    :param page_data: List of 2 tuples. The tuples contain the page data, title, position and wiki page_id
    :return: True if the player answer is correct, False otherwise.
    """
    first_page_title, first_latitude, first_longitude, first_page_id = page_data[0]
    second_page_title, second_latitude, second_longitude, second_page_id = page_data[1]

    print(f'\n{BRIGHT_YELLOW}{player} {RESET_STYLE}{BRIGHT_BLUE}"'
          f'which location is further east from the international dateline in the pacific? {RESET_STYLE}')

    player_answer = print_answer_options_and_get_answer(page_data, player_location)

    return player_answer == which_is_east((first_latitude, first_longitude),
                                          (second_latitude, second_longitude))


def ask_question_about_distance(player, player_location, page_data):
    """
    Ask the user which of the two locations are further away from them.
    :param player: player name
    :param player_location: player location
    :param page_data: List of 2 tuples. The tuples contain the page data, title, position and wiki page_id
    :return: True if the player answer is correct, False otherwise.
    """
    first_page_title, first_latitude, first_longitude, first_page_id = page_data[0]
    second_page_title, second_latitude, second_longitude, second_page_id = page_data[1]

    print(f'\n{BRIGHT_YELLOW}{player} {RESET_STYLE}{BRIGHT_BLUE}"'
          f'which location is further away from you?{RESET_STYLE}')

    player_answer = print_answer_options_and_get_answer(page_data, player_location)

    is_closer, distance_1_km, distance_2_km = compare_distance(
            player_location, (first_latitude, first_longitude), (second_latitude, second_longitude)
        )
    print(f"Your distance to {first_page_title} {pos_to_txt((first_latitude, first_longitude))} "
          f"is: {round(distance_1_km)}km,"
          f" and your distance to {second_page_title} {pos_to_txt((second_latitude, second_longitude))} "
          f"is: {round(distance_2_km)}km"
    )
    return player_answer != is_closer


def print_answer_options_and_get_answer(page_data, player_location):
    """
    Formats the wikipedia page data and adds a 2 sentence description of the page.
    Then asks the user which of the  pages and locations is the right answer.
    :param page_data: List of 2 tuples. The  tuples contain the page data, title, position and wiki page_id
    :param player_location: lat and lon of the player
    :return: 1 or 2 based on the user input
    """
    first_page_title, first_latitude, first_longitude, first_page_id = page_data[0]
    second_page_title, second_latitude, second_longitude, second_page_id = page_data[1]
    first_extract = get_extract(page_id=first_page_id, max_sentences=2)

    first_page_title_and_description = f"{UNDERLINE_START}{BOLD_START}{first_page_title}{RESET_STYLE}\n{first_extract}"
    second_extract = get_extract(page_id=second_page_id, max_sentences=2)
    second_page_title_and_description = f"{UNDERLINE_START}{BOLD_START}{second_page_title}{RESET_STYLE}\n{second_extract}"

    player_answer = get_user_input(first_page_title_and_description, second_page_title_and_description)

    print_locations([player_location, (first_latitude, first_longitude), (second_latitude, second_longitude)],
                    f"\n{RED}The two places and {BRIGHT_GREEN}you{RED} are here!{RESET_STYLE}")

    return player_answer


def play_one_round(player, player_location, points_until_now):
    """
    Play one round of the game.
    :param player: player whose turn it is to play
    :param player_location: Player location
    :param points_until_now: How many points the player has until now
    :return: New points from this round
    """
    page_data = get_random_page_with_coordinates2()
    match random.randint(1,3):
        case 1:
            round_result = ask_question_about_north(player, player_location, page_data)
        case 2:
            round_result = ask_question_about_east(player, player_location, page_data)
        case 3:
            round_result = ask_question_about_distance(player, player_location, page_data)
        case "_":
            raise RuntimeError("If we are here, something is broken in the code.")

    if round_result is True:
        round_points = 10
        print(f"{BRIGHT_GREEN}Correct{RESET_STYLE} {BRIGHT_YELLOW}{player}{RESET_STYLE}", end="")
    else:
        round_points = 0
        print(f"{BRIGHT_RED}Incorrect {BRIGHT_YELLOW}{player}{RESET_STYLE} ", end="")

    print(f"{BRIGHT_GREEN} you win {round_points} points. You have {points_until_now + round_points} points{RESET_STYLE}\n")

    return round_points


def play_the_game(player_names, player_locations, number_of_rounds):
    """
    The main game loop
    :param player_names: List of player names
    :param player_locations: List of player locations
    :param number_of_rounds: How many rounds shall we play
    :return: None
    """
    points_list = [0] * len(player_names)
    for player_num, player in enumerate(player_names):
        for _ in range(number_of_rounds):
            points_list[player_num] += play_one_round(player, player_locations[player_num], points_list[player_num])

    for key, p in enumerate(points_list):
        print(f'{BRIGHT_YELLOW}{player_names[key]}{RESET_STYLE} has {p} points')
    max_points = max(points_list)
    winning_players = [player_names[i] for i, p in enumerate(points_list) if p == max_points]

    if len(winning_players) == 1:
        print(f'\n{BRIGHT_YELLOW}{winning_players[0]}{RESET_STYLE} has the highest score with {max_points} points. 🎉')
    else:
        print(f'\nIt is a draw! {BRIGHT_YELLOW}{", ".join(winning_players)}{RESET_STYLE} have {max_points} points. 🎉')


def main():
    """
    Run the Guessipedia Challenge game.

    Players compete in a geography-based game by comparing locations
    based on their latitude, longitude, or distance from the player’s location.
    """
    introduce_game()
    number_of_rounds = get_number_of('rounds')
    player_names, player_locations = get_player_data()
    play_the_game(player_names, player_locations, number_of_rounds)


if __name__ == "__main__":
    main()
