import random
import statistics as st
import matplotlib.pyplot as plt
import movie_storage as movs
import os
import dotenv
from storage_csv import StorageCsv
import requests

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')
URL = 'https://api.api-ninjas.com/v1/animals'
HEADERS = {
    "X-Api-Key": API_KEY
}


class MovieApp:


    def __init__(self, storage = StorageCsv("movies.csv")):
        self._storage = storage


    @staticmethod
    def _values_of_movies(movies):
        """ This function gets the movie data and returns total of values (as a float),
        rating values (as a list), amount of movies (as an integer), movie names in normal case and lowercase (as a list),
        and the movie year (as a list)
        """

        total_of_values = 0
        rating_values = []
        amount_of_movies = 0
        movie_names = []
        movie_names_lowercase = []  # for easier searching and deletion
        movie_years = []
        for movie_name, movie_info in movies.items():
            amount_of_movies += 1
            total_of_values += float(movie_info["rating"])
            rating_values.append(movie_info["rating"])
            movie_names.append(movie_name)
            movie_years.append(movie_info["year"])
            lowercase_movie = movie_name.lower()
            movie_names_lowercase.append(lowercase_movie)
        return (total_of_values, rating_values, amount_of_movies,
                movie_years, movie_names, movie_names_lowercase)


    @staticmethod
    def _exit_function():
        """ Exits the program """
        print("Bye!")
        return exit()


    def _command_list_movies(self):
        """ Prints a list of all movies """
        movies = self._storage.list_movies()
        print(f'{self._values_of_movies(movies)[2]} movies in total')

        for movie_name, movie_info in movies.items():
            name = movie_name
            rating = movie_info["rating"]
            year = movie_info["year"]
            print(f'{name} ({year}): {rating}')

    @staticmethod
    def _fetch_movie_from_api(movie_name):
        """Fetch movie details from the OMDB API."""
        api_url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                return {
                    "title": data.get("Title"),
                    "year": data.get("Year"),
                    "rating": float(data.get("imdbRating", 0)),
                    "poster": data.get("Poster")
                }
        return None

    def _add_movie(self):
        """ Adds a new movie to the list """
        movie_to_add = input("Enter new movie name:  ").strip()
        if not movie_to_add:
            print("Movie name cannot be empty")
            return

        movies = self._storage.list_movies()

        for movie_name in movies.keys():
            if movie_name.lower() == movie_to_add.lower():
                print("Movie already exists")
                return

        movie_details = self._fetch_movie_from_api(movie_to_add)
        if movie_details:
            print(f"movie found: {movie_details['title'], 
            movie_details['year'], movie_details['rating'], 
            movie_details['poster']}")
            confirmation = input("Do you want to add this movie? (y/n): ").strip().lower()
            if confirmation != 'y':
                return
        else:
            print("Movie not found in API. Enter details manually.")
            movie_details = {
                "title": movie_to_add,
                "year": input("Enter movie year (4 digits): ").strip(),
                "rating": float(input("Enter movie rating between 0 and 10: ").strip()),
                "poster": None
            }
        self._storage.add_movie(movie_details["title"],
                                movie_details["year"],
                                movie_details["rating"],
                                movie_details["poster"])
        print("Movie added successfully")


    def _delete_movie(self):
        """ Deletes a movie from the list """
        movie_to_delete = input("Which movie would you like to delete? ")
        movies = self._storage.list_movies()
        for movie_name in movies.keys():
            if movie_to_delete == "":
                print("Please enter a movie name")
                return
            if movie_name.lower() == movie_to_delete.lower():
                movs.delete_movie_storage(movie_name)
                print('Movie deleted successfully')
                return
        print("Movie not found")


    def _update_movie(self):
        """ Updates a movie in the list """
        movie_to_update = input("Enter movie name: ").strip()
        movies = self._storage.list_movies()
        for movie_name, movie_info in movies.items():
            if movie_name.lower() == movie_to_update.lower():
                try:
                    rating_to_update = float(input("Enter new movie rating between 0 and 10: "))
                except ValueError:
                    print("Expected a positive integer.")
                    return
                if rating_to_update < 0 or rating_to_update > 10:
                    print("Rating must be between 0 and 10")
                    return
                movs.update_movie_storage(movie_name, rating_to_update)
                print('Movie updated successfully')
                return
        else:
            print("Movie not found")


    def _stats_from_movies(self):
        """ Prints statistics about the movies """
        movies = self._storage.list_movies()
        values = self._values_of_movies(movies)

        average_value = round(st.mean(values[1]), 2) if values[1] else 0
        median_value = st.median(values[1]) if values[1] else 0
        best_movie = max(movies.items(), key=lambda x: x[1]["rating"], default=None)
        worst_movie = min(movies.items(), key=lambda x: x[1]["rating"], default=None)

        print(f"\nAverage rating: {average_value}")
        print(f"\nMedian rating: {median_value}")

        if best_movie:
            print(f"Best movie: {best_movie[0]} ({best_movie[1]['rating']})")
        if worst_movie:
            print(f"Worst movie: {worst_movie[0]} ({worst_movie[1]['rating']})")


    def _random_movie(self):
        """ Prints a random movie """
        try:
            movies = self._storage.list_movies()
            random_movie_name = random.choice(self._values_of_movies(movies)[3])
            random_movie_rating = ""
            for movie_name, movie_info in movies.items():
                if movie_name == random_movie_name:
                    random_movie_rating = movie_info["rating"]
            print(f"Your movie for tonight: {random_movie_name}, "
                  f"it's rated {random_movie_rating}")
        except KeyError:
            print("No movies found.")


    def _find_movie(self):
        """ Finds a movie based on a keyword """
        keyword= input ("Enter a keyword: ")
        lowercase_keyword= keyword.lower().strip()
        movies = self._storage.list_movies()
        found_movie = False
        _, _, _, _, movie_names, lowercase_movie_names = self._values_of_movies(movies)

        for i, lowercase_movie in enumerate(lowercase_movie_names):
            if lowercase_keyword in lowercase_movie:
                print (movie_names[i])
                found_movie = True

        if not found_movie:
            print ("No movies found")


    def _movies_by_rating(self):
        """ Prints movies sorted by rating """
        movies = self._storage.list_movies()
        sorted_ratings = sorted(movies.items(),
                                key=lambda item: item[1]["rating"], reverse=True)
        for movie_name, movie_info in sorted_ratings:
            print(f'{movie_name}: {movie_info["rating"]}')


    def _rating_histogram(self):
        """ Saves a histogram of the ratings """
        user_folder = input("Save histogram in file: ")
        if not user_folder.endswith((".png", ".jpeg")):
            user_folder += ".png"
        movies = self._storage.list_movies()
        ratings = self._values_of_movies(movies)[1]
        plt.hist(ratings, bins=5, edgecolor='blue')
        plt.title("Movie Rating Histogram")
        plt.xlabel("Ratings")
        plt.ylabel("Number of Movies")
        plt.savefig(user_folder)
        plt.close()
        print(f"Histogram saved as {user_folder}")


    def _generate_website(self):
        """Generates a website for the movie collection."""
        try:
            # Read the template
            with open("index_template.html", "r", encoding="utf-8") as file:
                template_content = file.read()

            # Replace placeholders
            updated_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie Collection")
            updated_content = updated_content.replace("__TEMPLATE_MOVIE_GRID__",
                                                      self._storage.generate_movies_html())

            # Write the final HTML
            with open("index.html", "w", encoding="utf-8") as file:
                file.write(updated_content)

            print("Website generated successfully: index.html")
        except FileNotFoundError:
            print("Template file not found. Ensure 'index_template.html' exists.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _menu_user_input(self):
        """ Menu displayed to user """
        menu = ('Menu:\n0. Exit.\n1. List movies.\n2. Add movie.\n3. Delete movie.'
                '\n4. Update movie.\n5. Stats.\n6. Random movie.\n7. Search movie.'
                '\n8. Movies sorted by rating.\n9. Histogram.\n10. Generate website.')
        print(menu)

        try:
            action = int(input("Enter choice (0-9):"))
            if action in range(0, 11):
                return action
            else:
                print("\nPlease enter a valid choice!\n")
                return self._menu_user_input()
        except ValueError:
            return


    def run(self):
        """ Main function of the program """
        while True:
            number_chosen = self._menu_user_input()
            function_dictionary = {
                0: self._exit_function,
                1: self._command_list_movies,
                2: self._add_movie,
                3: self._delete_movie,
                4: self._update_movie,
                5: self._stats_from_movies,
                6: self._random_movie,
                7: self._find_movie,
                8: self._movies_by_rating,
                9: self._rating_histogram,
                10: self._generate_website
            }
            try:
                chosen_function = function_dictionary[number_chosen]
                if chosen_function == self._exit_function:
                    chosen_function()
                else:
                    chosen_function()
                input("\nPress enter to continue...")
            except (ValueError, KeyError) as e:
                print(e)
                print("\nEnter a number between 0 and 9.\n")


