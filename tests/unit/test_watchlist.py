import pytest

from covid.domain.model import Movie, WatchList

def test_watchList():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie2 = Movie(1, "Ronald Weasley", 2010, "Wizards")
    movie3 = Movie(2, "Hermione Granger", 2010, "Wizards")
    watchlist1 = WatchList()
    watchlist1.add_movie(movie1)
    watchlist1.add_movie(movie2)
    watchlist1.add_movie(movie3)
    assert watchlist1.watch_list == [movie1, movie2, movie3]

def test_remove_watchList():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie2 = Movie(1, "Ronald Weasley", 2010, "Wizards")
    movie3 = Movie(2, "Hermione Granger", 2010, "Wizards")
    watchlist1 = WatchList()
    watchlist1.add_movie(movie1)
    watchlist1.add_movie(movie2)
    watchlist1.add_movie(movie3)
    watchlist1.remove_movie(movie3)
    assert watchlist1.watch_list == [movie1, movie2]

def test_same_watchList_movie():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    watchlist1 = WatchList()
    watchlist1.add_movie(movie1)
    towatch = watchlist1.select_movie_to_watch(0)
    assert towatch == movie1

def test_watchList_size():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie2 = Movie(1, "Ronald Weasley", 2010, "Wizards")
    watchlist1 = WatchList()
    watchlist1.add_movie(movie1)
    watchlist1.add_movie(movie2)
    assert watchlist1.size() == 2

def test_watchList_first():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie2 = Movie(1, "Ronald Weasley", 2010, "Wizards")
    watchlist1 = WatchList()
    watchlist1.add_movie(movie1)
    watchlist1.add_movie(movie2)
    first = watchlist1.first_movie_in_watchlist()
    assert first == movie1