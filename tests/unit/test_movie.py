import pytest

from covid.domain.model import Movie, Director, Actor, Genre

@pytest.fixture
def movie():
    return Movie(0, "Harry Potter", 2010, "Wizards")

def test_movie(movie):
    assert repr(movie) == "<Movie Harry Potter, 2010>"

def test_init():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    assert movie1.title == "Harry Potter"
    assert movie1.year == 2010

def test_movie_description():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie1.description = "Wizard Movie"
    assert movie1.description == "Wizard Movie"

def test_movie_director():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie1.director = Director("Ronald Weasley")
    assert movie1.director == Director("Ronald Weasley")
    movie1.director = Director("Albus Dumbledore")
    assert movie1.director == Director("Albus Dumbledore")

def test_movie_actors():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    assert movie1.actors == []
    movie1.actors = Actor("Hermione Granger")
    assert movie1.actors == [Actor("Hermione Granger")]
    movie1.actors = Actor("Rubius Hagrid")
    assert movie1.actors == [Actor("Hermione Granger"), Actor("Rubius Hagrid")]
    movie1.add_actor(Actor("Severus Snape"))
    assert movie1.actors == [Actor("Hermione Granger"), Actor("Rubius Hagrid"), Actor("Severus Snape")]
    movie1.remove_actor(Actor("Severus Snape"))
    assert movie1.actors == [Actor("Hermione Granger"), Actor("Rubius Hagrid")]

def test_movie_genres():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    assert movie1.genres == []
    movie1.genres = Genre("Fantasy")
    assert movie1.genres == [Genre("Fantasy")]
    movie1.genres = Genre("Adventure")
    assert movie1.genres == [Genre("Fantasy"), Genre("Adventure")]
    movie1.add_genre(Genre("Wizard"))
    assert movie1.genres == [Genre("Fantasy"), Genre("Adventure"), Genre("Wizard")]
    movie1.add_genre(Genre("Wizard"))
    assert movie1.genres == [Genre("Fantasy"), Genre("Adventure"), Genre("Wizard")]
    movie1.remove_genre(Genre("Wizard"))
    assert movie1.genres == [Genre("Fantasy"), Genre("Adventure")]

def test_movie_runtime():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    assert movie1.runtime_minutes == 0
    movie1.runtime_minutes = 100
    assert movie1.runtime_minutes == 100

def test_movie_same():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    assert movie1 == movie1

def test_movie_different():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    movie2 = Movie(1, "Ronald Weasley", 2010, "Wizards")
    assert movie1 != movie2

def test_movie_more():
    movie2 = Movie(1, "Ronald Weasley", 2010, "Wizards")
    movie3 = Movie(1, "Ronald Weasley", 2011, "Wizards")
    assert movie2 < movie3
    
def test_movie_hash():
    movie1 = Movie(0, "Harry Potter", 2010, "Wizards")
    assert hash(movie1) == hash(movie1)
    