"""MovieApp uses the Storage instance to store and retrieve movie data.
UserShell interacts with the user and calls the appropriate methods on MovieApp."""
import shutil
from storage import StorageJson, StorageCsv, StorageError, os, json
import movies_storage as webCalls
from movies_storage import FunctionErrors
import ioput as io

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
FOLDER_DIR = os.path.join(SCRIPT_DIR, "STORAGE")


class AppError(Exception):
    """AppError is a class for raising errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class UserShellError(Exception):
    """UserShellError is a class for raising errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class MovieApp():
    """Function calls for Storage instances"""

    @staticmethod
    def validate_storage(storage):
        """Validates the storage instance."""
        if not isinstance(storage, (StorageJson, StorageCsv)):
            raise AppError("Invalid storage instance")

    @staticmethod
    def format_movie_data(movie_data):
        """Checks key values in movie_data."""
        if not movie_data["Title"]:
            raise AppError("Movie title is missing")
        movie_data["Title"] = movie_data["Title"].strip().title()
        if not movie_data["Year"]:
            raise AppError("Movie year is missing")
        if not movie_data["imdbRating"]:
            raise AppError("Movie rating is missing")
        movie_data["imdbRating"] = float(movie_data["imdbRating"])
        return movie_data

    @staticmethod
    def read_movie_name(movie_name):
        """Ignore invalid user input. Format user entered movie name."""
        while True:
            try:
                # movie_name = input(prompt)
                if movie_name.strip() == "":
                    raise AppError("Please do not leave empty")
                movie_name = movie_name.strip().title()
                return movie_name
            except AppError as app_error:
                print(app_error)
            except KeyboardInterrupt:
                print("Do not interrupt the process")

    def __init__(self, storage) -> None:
        self._storage = storage

    def add_movie(self):
        """Adds a movie to the destinated movies database."""
        saved_movies = self._storage.list_movies()
        movie_name = MovieApp.read_movie_name(input("Enter movie name: "))
        if movie_name in saved_movies:
            raise AppError("Movie already exists in database")
        movie_data = webCalls.get_by_name(movie_name)
        movie_data = MovieApp.format_movie_data(movie_data)
        name = movie_data.get("Title", None)
        year = movie_data.get("Year", None)
        rating = movie_data.get("imdbRating", None)
        poster = movie_data.get("Poster", None)
        self._storage.add_movie(name, year, rating, poster)
        return f"Movie {name} added successfully"

    def list_movies(self):
        """Returns a list of movies in the database."""
        movies = self._storage.list_movies()
        if len(movies) == 0:
            raise AppError("No movies in database")
        template = "\n".join(
            f"{x[0]}. {x[1][0]}, Year: {x[1][1]['Year']}, Rating: {x[1][1]['imdbRating']}"
            for x in enumerate(movies.items(), start=1))
        return template

    def delete_movie(self, movie_name: str):
        """Deletes a movie from the database."""
        movie_name = MovieApp.read_movie_name(movie_name)
        movies = self._storage.list_movies()
        if movie_name not in movies:
            raise AppError("Movie doesn't exist in database")
        self._storage.delete_movie(movie_name)
        return f"Movie {movie_name} deleted successfully"

    def update_movie(self, movie_name: str, rating: float):
        """Updates a movie's rating in the database."""
        movie_name = MovieApp.read_movie_name(movie_name)
        movies = self._storage.list_movies()
        if movie_name not in movies:
            raise AppError("Movie doesn't exist in database")
        self._storage.update_movie(movie_name, rating)
        return f"Movie {movie_name} updated successfully"

    def sort_movies(self):
        """Use movies_storage.py to sort movies."""
        return webCalls.get_sort_movies(self._storage)

    def stat_movies(self):
        """Use movies_storage.py to get stat of movies."""
        return webCalls.get_stat_movies(self._storage)

    def __str__(self):
        return f"MovieApp connected directory:\n({self._storage.file_path})"


class UserShell:
    """User Interface class for the movie app
    Sets user file path for write and read"""
    _registry = os.path.join(SCRIPT_DIR, "registry")
    _write_html = os.path.join(SCRIPT_DIR, "_static")

    def __init__(self, user_data: dict) -> None:
        self.user_name = user_data["username"].strip().lower()
        self.password = user_data["password"]

    def registry_dir(self):
        """get registry folder"""
        if not os.path.exists(UserShell._registry):
            os.makedirs(UserShell._registry)
        return UserShell._registry

    def user_registry_folder_dir(self):
        """get folder path"""
        registry_folder_path = os.path.join(
            self.registry_dir(), f'{self.user_name}')
        if not os.path.exists(registry_folder_path):
            os.makedirs(registry_folder_path)
        return registry_folder_path

    def user_registry_path(self):
        """get registry path"""
        return os.path.join(
            self.user_registry_folder_dir(), "registry.json")

    def get_user_movie_path(self):
        """set user movie path"""
        if not os.path.exists(FOLDER_DIR):
            os.makedirs(FOLDER_DIR)
        return os.path.join(FOLDER_DIR, f"{self.user_name}")

    def get_app(self, file_path) -> None:
        """get MovieApp instance for user"""
        return MovieApp(file_path)

    def get_html_index(self):
        """get html index"""
        return os.path.join(SCRIPT_DIR, "_static", "index_template.html")

    def get_updated_path(self):
        """get updated html path"""
        return os.path.join(UserShell._write_html, f"{self.user_name}.html")

    def generate_user_webpage(self, istorage):
        """generate user webpage"""
        return webCalls.create_webpage(self, istorage)

    def registry(self) -> str:
        """Create a user file if it doesn't exist"""
        user_data = {
            "username": self.user_name,
            "password": self.password
        }
        with open(self.user_registry_path(), "w", encoding="utf-8") as registry:
            json.dump(user_data, registry)
        print("NEW USER APPLICATION COMPLETED")

    def is_password_correct(self) -> bool:
        """Check user instance password info in registry"""
        if not os.path.exists(self.user_registry_path()):
            directory_to_delete = self.user_registry_folder_dir()
            shutil.rmtree(directory_to_delete)
            raise UserShellError("User is not registered!! Aborted")
        with open(self.user_registry_path(), "r", encoding="utf-8") as registry:
            user_data = json.load(registry)
        return user_data["password"] == self.password


def get_name_and_password():
    """Takes user name and password"""
    user_name = io.read_text("Please Enter your name: ")
    user_password = io.read_text("Please enter your password: ")
    user_data = {
        "username": user_name,
        "password": user_password
    }
    return user_data


def checking_sign_info():
    """Checks user registry info"""
    if io.ask_to_continue("Have you been registed before y/n: "):
        user_info = get_name_and_password()
        user = UserShell(user_info)
        if not user.is_password_correct():
            raise UserShellError("Password is not correct!! Aborted")
        print("USER SIGN IN VALIDATED")
    else:
        if io.ask_to_continue("Do you want to sign in y/n: "):
            user_info = get_name_and_password()
            user = UserShell(user_info)
            user.registry()
        else:
            raise UserShellError("APPLICATION IS ABORTED")
    return user


def get_user_storage(file_extension, user_movie_path):
    """Get the appropriate user storage based on file extension."""
    if file_extension.strip().lower() == "csv":
        return StorageCsv(user_movie_path)
    if file_extension.strip().lower() == "json":
        return StorageJson(user_movie_path)
    raise UserShellError("File extension is not valid!! Aborted")


def perform_movie_operation(user, user_storage, operation, command):
    """Perform the selected movie operation."""
    if command == 3:
        movie_name = io.read_text("Enter a movie name: ")
        print(f"\n{operation[command](movie_name)}\n")
    elif command == 4:
        movie_name = io.read_text("Enter a movie name: ")
        new_rating = io.read_float("Enter a new rating: ")
        print(f"\n{operation[command](movie_name, new_rating)}\n")
    elif command == 7:
        print(f"\n{user.generate_user_webpage(user_storage)}\n")
    else:
        print(f"\n{operation[command]()}\n")


def user_menu():
    """Take user name and password to set UserShell instance
    and set storage type instance file path by given UserShell file path properties
    connect 3 instance to MovieApp class and run MovieApp class methods"""
    try:
        # Assigns UserShell instance to user variable
        user = checking_sign_info()
        file_extension = io.read_text(
            "Please enter file extension (json/csv): ")
        user_movie_path = user.get_user_movie_path()
        # Assigns StorageJson or StorageCsv instance to user_storage variable
        user_storage = get_user_storage(file_extension, user_movie_path)
        # Assigns MovieApp instance to user_app variable
        user_app = user.get_app(user_storage)

        operation = {
            1: user_app.list_movies,
            2: user_app.add_movie,
            3: user_app.delete_movie,
            4: user_app.update_movie,
            5: user_app.sort_movies,
            6: user_app.stat_movies,
            7: user.generate_user_webpage,
            8: "exit"
        }

        # exclude_functions = []
        # if isinstance(user_storage, StorageCsv):
        #     exclude_functions = [user_app.stat_movies,
        #                          user.generate_user_webpage]

        operation_text = "\n".join(
            f"{x[0]}. {x[1].__name__.replace('_', ' ').title()}"
            if callable(x[1]) else f"{x[0]}. {x[1]}"
            for x in enumerate(operation.values(), start=1))

        while True:
            try:
                command = io.read_int_ranged("\tOPERATIONS\n" +
                                             operation_text + "\nChosen command: ",
                                             1, len(operation))
                if command == len(operation):
                    break
                perform_movie_operation(user, user_storage, operation, command)
            except (AppError, StorageError, FunctionErrors) as error:
                print(f"Application or Storage\n\t-->{error}")
                continue
    except UserShellError as error:
        print(f"Application terminated\n\t--> {error}")


def main():
    """main function"""
    user_menu()


if __name__ == "__main__":
    main()
