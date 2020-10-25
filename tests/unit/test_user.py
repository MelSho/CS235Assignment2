import pytest

from covid.domain.model import Movie, User

def test_user():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie1.runtime_minutes = 100
    assert movie1.runtime_minutes == 100
    user1 = User("Hermione Granger", "hp100")
    assert user1.username == "hermione granger"
    assert user1.password == "hp100"
    assert user1.watched_movies == []
    assert user1.reviews == []
    assert user1.time_spent_watching_movies_minutes == 0

def test_user_watchtime():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie1.runtime_minutes = 100
    assert movie1.runtime_minutes == 100
    user1 = User("Hermione Granger", "hp100")
    user1.watch_movie(movie1)
    assert user1.watched_movies == [movie1]
    assert user1.time_spent_watching_movies_minutes == 100

def test_user_reviews():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie1.runtime_minutes = 100
    assert movie1.runtime_minutes == 100
    user1 = User("Hermione Granger", "hp100")
    user1.add_review("wow so good i love harry potter")
    assert user1.reviews == ["wow so good i love harry potter"]