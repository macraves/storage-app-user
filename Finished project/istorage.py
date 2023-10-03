"""Interface for storage classes"""
from abc import ABC, abstractmethod


class IStorage(ABC):
    """METHODS for storage classes"""
    @abstractmethod
    def list_movies(self):
        """list_movies is a method that returns a dictionary."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """add_movie is a method that returns a dictionary."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """delete_movie is a method that returns a dictionary."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """update_movie is a method that returns a dictionary."""
        pass

    # create a list of 100 numbers from 0 to 99

    # odd_numbers = [x for x in range(100) if x % 2 == 1]
