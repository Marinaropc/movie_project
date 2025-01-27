from storage.storage_csv import StorageCsv
from movie_app import MovieApp

if __name__ == "__main__":
    storage = StorageCsv("data/movies.csv")
    app = MovieApp(storage)
    app.run()