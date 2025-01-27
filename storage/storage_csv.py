from storage.istorage import IStorage
import csv


class StorageCsv(IStorage):
    def __init__(self, file_path):
        """
        Initializes the storage with the file path
        """
        self.file_path = file_path

    def list_movies(self):
        """Reads file and returns a dictionary of movies"""
        movies = {}
        try:
            with open(self.file_path, 'r', encoding="utf-8") as fileobj:
                reader = csv.DictReader(fileobj)

                # Check if the file has no rows
                if reader.fieldnames is None:
                    print("CSV file is empty or has no header!")  # Debugging
                    return {}

                for row in reader:
                    # Ensure all required keys exist in the row
                    if all(key in row for key in ["title", "year", "rating", "poster"]):
                        title = row["title"]

                        movies[title] = {
                            'year': int(row['year']) if row['year'].isdigit() else 0,
                            'rating': float(row['rating']) if row['rating'].replace('.', '', 1).isdigit() else 0.0,
                            'poster': row.get('poster', '')
                        }
                    else:
                        print(f"Malformed row: {row}")  # Debugging
        except FileNotFoundError:
            print("File not found!")  # Debugging
            return {}
        except Exception as e:
            print(f"Unexpected error: {e}")  # Debugging for other issues
            return {}

        return movies

    def save_movies_storage(self, movie_dict):
        """Saves a dictionary of movies to the file"""
        with open(self.file_path, 'w', encoding="utf-8", newline='') as fileobj:
            fieldnames = ['title', 'year', 'rating', 'poster']
            writer = csv.DictWriter(fileobj, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movie_dict.items():
                writer.writerow({
                    'title': title,
                    'year': details['year'],
                    'rating': details['rating'],
                    'poster': details.get('poster', '')  # Handle missing poster
                })

    def add_movie(self, title, year, rating, poster=""):
        """Adds a movie to the file"""
        movies_dict = self.list_movies()
        movies_dict[title] = {
            "year": int(year),
            "rating": float(rating),
            "poster": poster
        }
        self.save_movies_storage(movies_dict)

    def delete_movie(self, title):
        """Deletes a movie from the file"""
        movies_dict = self.list_movies()
        if title in movies_dict:
            del movies_dict[title]
            self.save_movies_storage(movies_dict)

    def update_movie(self, title, rating):
        """Updates a movie's rating in the file"""
        movies_dict = self.list_movies()
        if title in movies_dict:
            movies_dict[title]["rating"] = float(rating)
            self.save_movies_storage(movies_dict)

    def generate_movies_html(self):
        """Generates HTML content for the movie grid."""
        movies = self.list_movies()  # Get the dictionary of movies
        movie_html = ""

        for title, details in movies.items():
            year = details["year"]
            rating = details["rating"]
            poster_url = details.get("poster", "")

            # Construct the HTML for each movie
            movie_html += f"""
                <li>
                    <div class="movie">
                        <img class="movie-poster" src="{poster_url}" alt="{title}" style="height: 200px;">
                        <div class="movie-title">{title}</div>
                        <div class="movie-year">Year: {year}</div>
                        <div class="movie-rating">Rating: {rating}</div>
                    </div>
                </li>
            """

        return movie_html
