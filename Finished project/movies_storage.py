"""Methods for stored objects in a file."""
import requests
from storage import json

YOUR_API_KEY = "ae98550b"
BASE_URL = "http://www.omdbapi.com"


class FunctionErrors(Exception):
    """FunctionErrors is a class for raising errors."""

    def __init__(self, message: object) -> None:
        super().__init__(message)


def get_name_method_requests(method_name: str, movie_name: str) -> str:
    """Sets the  movie name search end point method.
    Args:
        method_name (str): "name" string.
        movie_name (str): given string by user.
    Returns:
        str: returns whole url modified by user input.
    """
    method_api = {
        "name": f"{BASE_URL}/?t={movie_name}&apikey={YOUR_API_KEY}"
    }
    if method_name in method_api:
        return method_api[method_name]
    return None


def get_by_name(movie_name: str) -> dict:
    """get_by_name is a method that returns a dict.
    Args:
        movie_name (str): given string by user.
    Returns:
        parsed_data: returns dictionary of movie.
    """
    request_api = get_name_method_requests("name", movie_name)
    if request_api is not None:
        try:
            response = requests.get(request_api, timeout=5)
            parsed_data = json.loads(response.text)
            # Check for HTTP error status codes
            response.raise_for_status()
            response_status = parsed_data.get("Response", "Unknown")
            title_status = parsed_data.get("Title", "Unknown")
            # Unvalid user text returns Response: False
            if not response_status == "True" or title_status == "Unknown":
                raise FunctionErrors(
                    f"Entered movie name: {movie_name} has no response")
            return parsed_data
        except requests.exceptions.RequestException as rer:
            raise FunctionErrors(
                f"Error requesting page {request_api}:\n\t--> {rer}") from rer
    return None


def get_sort_movies(instance):
    """
    Sorts the movies database.
    Loads the information from the file, sorts the movies,
    The function doesn't need to validate the input.
    """
    data = instance.list_movies()
    valid_entries = {"asc": False, "desc": True}
    user_choice = input("Enter the order of sorting 'asc' or 'desc': ")
    if not user_choice.strip().lower() in valid_entries:
        raise FunctionErrors("Invalid sorting input")

    sorted_movies = sorted(
        data.items(), key=lambda x: float(x[1]['imdbRating']),
        reverse=valid_entries[user_choice])
    return "\n".join(
        f"{item[0]}. {item[1][0]}, Year: {item[1][1]['Year']}, Rating: {item[1][1]['imdbRating']}"
        for item in enumerate(sorted_movies, start=1))


def get_stat_movies(instance):
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.
    """
    data = instance.list_movies()
    max_rating = max(data.values(), key=lambda x: float(x['imdbRating']))
    min_rating = min(data.values(), key=lambda x: float(x['imdbRating']))
    average_rating = sum(float(item['imdbRating'])
                         for item in data.values()) / len(data)

    return f"""Max rating: {max_rating['imdbRating']}
Min rating: {min_rating['imdbRating']}
Average rating: {average_rating:.2f}"""


def create_movies_list_html(movies):
    """Create a list of movies in html format"""
    # target = "__TEMPLATE_MOVIE_GRID__"
    html_code = []
    for key, value in movies.items():
        template = '''<li>
            <div class="movie">
                <img class="movie-poster"
                     src={poster}
                     title=""/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{year}</div>
            </div>
        </li>'''
        title = key
        year = value["Year"]
        poster = value["Poster"]

        template = template.format(
            poster=poster, title=title, year=year)
        html_code.append(template)
    return "\n".join(html_code)


def replace_in_html(user, replacement):
    """Replace target in html file with replacement"""

    with open(user.get_html_index(), "r", encoding="utf-8") as current_html:
        with open(user.get_updated_path(), "w", encoding="utf-8") as new_html:
            source_html = current_html.read()
            updated_html = source_html.replace(
                "My Movie App", "RAVEN MACIUS")
            updated_html = updated_html.replace(
                "__TEMPLATE_TITLE__", "MY MOVIE DATABASE")
            updated_html = updated_html.replace(
                "__TEMPLATE_MOVIE_GRID__", replacement)
            new_html.write(updated_html)


def create_webpage(user, instance):
    """Main generate user webpage function"""
    movies_data = instance.list_movies()
    html_str = create_movies_list_html(movies_data)
    replace_in_html(user, html_str)
    return "HTML file created successfully"
