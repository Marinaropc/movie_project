import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, '..', 'data', 'movie_data.json')


def get_movies_storage():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.
    """

    with open(json_file_path, 'r') as fileobj:
        movies_dict = json.load(fileobj)
    return movies_dict


def save_movies_storage(movie):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(json_file_path, 'w') as fileobj:
        json.dump(movie, fileobj)


def add_movie_storage(title, year, rating):
    """
    Adds a movie to the movie database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    try:
        with open(json_file_path, 'r') as fileobj:
            movies_dict = json.load(fileobj)
    except FileNotFoundError:
        movies_dict = {}
    movies_dict[title] = {"rating": rating, "year": year}
    save_movies_storage(movies_dict)


def delete_movie_storage(title):
    """
    Deletes a movie from the movie database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    with open(json_file_path, 'r') as fileobj:
        movies_dict = json.load(fileobj)
    movies_dict.pop(title)
    save_movies_storage(movies_dict)


def update_movie_storage(title, rating):
    """
    Updates a movie from the movie database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    with open(json_file_path, 'r') as fileobj:
        movies_dict = json.load(fileobj)
    movies_dict[title]["rating"] = rating
    save_movies_storage(movies_dict)
