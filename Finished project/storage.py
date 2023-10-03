"""Methods for json data to the database."""

import os
import csv
import json
from istorage import IStorage


class StorageError(Exception):
    """StorageError is a class for raising errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class StorageJson(IStorage):
    """This class is used to store movies in a json file."""

    def __init__(self, file_path):
        """Recive file path with name without extension"""
        file_path = file_path + ".json"
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump({}, json_file, indent=4)
        self._file_path = file_path

    def _read_file(self):
        """Reads the data from the file and returns it as a dictionary."""
        try:
            with open(self._file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
            return data
        except json.decoder.JSONDecodeError as jdecoder:
            raise StorageError(
                f"Error decoding json file {self._file_path}:\n\t--> {jdecoder}") from jdecoder

    def _write_file(self, data):
        """Writes the data to the file."""
        with open(self._file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    def list_movies(self):
        """Returns a dictionary of dictionaries that"""
        data = self._read_file()
        return data

    def add_movie(self, title, year, rating, poster) -> None:
        """Adds a movie to the movies database."""
        data = self._read_file()
        if title in data:
            raise StorageError("Movie already exists in json file")
        data[title] = {"Year": year, "imdbRating": rating, "Poster": poster}
        self._write_file(data)

    def delete_movie(self, title):
        """Deletes a movie from the movies database."""
        data = self._read_file()
        if title not in data:
            raise StorageError("Movie doesn't exist in json file")
        del data[title]
        self._write_file(data)

    def update_movie(self, title, rating):
        """Updates a movie's rating in the JSON file."""
        data = self._read_file()
        if title in data:
            data[title]["imdbRating"] = float(rating)
            self._write_file(data)
        else:
            raise StorageError("Movie doesn't exist in json file")

    def __str__(self):
        movies = self._read_file()
        movies_map = map(lambda item:
                         f"{item[0]}. {item[1][0]}, Year: {item[1][1]['Year']}, imdbRating: {item[1][1]['imdbRating']}",
                         enumerate(movies.items(), start=1))
        return "\n".join(movies_map)


class StorageCsv(IStorage):
    """This class is used to store movies in a csv file."""

    def __init__(self, file_path):
        """Recive file path with name without extension"""
        file_path = file_path + ".csv"
        self._file_path = file_path
        if not os.path.exists(file_path):
            self._initialize_csv()

    def _initialize_csv(self):
        """Initializes the CSV file with a header row"""
        with open(self._file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=[
                                    "Title", "Year", "imdbRating", "Poster"])
            writer.writeheader()

    def _read_file(self):
        """Method of csv.DictReader returns a list of dictionaries.
        Each dictionary is a row in the csv file. This function iterates
        list and all list items are  dictionaries. Assigns the key of the
        dictionary to the title and the value to the dictionary."""
        try:
            with open(self._file_path, "r", newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                data = {}
                for row in reader:
                    data[row["Title"]] = {
                        "Year": row["Year"], "imdbRating": row["imdbRating"], "Poster": row["Poster"]}
            return data
        except csv.Error as csverror:
            raise StorageError(
                f"Error reading csv file {self._file_path}:\n\t--> {csverror}") from csverror

    def _write_file(self, data: dict):
        """Writes the data as the form of a dictionary to the file."""
        with open(self._file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["Title", "Year", "imdbRating", "Poster"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for title, info in data.items():
                writer.writerow({"Title": title, "Year": info["Year"],
                                "imdbRating": info["imdbRating"], "Poster": info["Poster"]})

    def _append_file(self, data):
        """Appends the data to the file."""
        with open(self._file_path, mode="a", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["Title", "Year", "imdbRating", "Poster"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({"Title": data["Title"], "Year": data["Year"],
                             "imdbRating": data["imdbRating"], "Poster": data["Poster"]})

    def list_movies(self):
        """list_movies is a method that returns a dictionary."""
        return self._read_file()

    def add_movie(self, title, year, rating, poster):
        """If there is not duplication checks file size
        Uses _write_file for empty files otherwise _append_file method."""
        new_data = {}
        if title in self._read_file():
            raise StorageError("Movie already exists in csv file")
        new_data = {"Title": title, "Year": year,
                    "imdbRating": rating, "Poster": poster}
        if os.path.getsize(self._file_path) == 0:
            self._write_file(new_data)
        else:
            self._append_file(new_data)

    def delete_movie(self, title):
        """delete_movie is a method that returns a dictionary."""
        movies = self._read_file()
        if title not in movies:
            raise StorageError("Movie not found in csv file")
        del movies[title]
        self._write_file(movies)

    def update_movie(self, title, rating):
        """update_movie is a method that returns a dictionary."""
        movies = self._read_file()
        if title not in movies:
            raise StorageError("Movie not found in csv file")
        movie = movies[title]
        movie["imdbRating"] = rating
        self._write_file(movies)
