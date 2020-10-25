import pytest

from covid.domain.model import Genre

@pytest.fixture
def genre():
    return Genre("Fantasy")

def test_genre(genre):
    assert repr(genre) == "<Genre Fantasy>"

def test_init():
    genre1 = Genre("Comedy")
    assert repr(genre1) == "<Genre Comedy>"

def test_genre_none():
    genre2 = Genre("")
    assert genre2.genre_name is None
    genre3 = Genre(42)
    assert genre3.genre_name is None

def test_genre_same():
    genre1 = Genre("Comedy")
    assert genre1 == genre1

def test_genre_different():
    genre1 = Genre("Comedy")
    genre4 = Genre("Horror")
    assert genre1 < genre4

def test_genre_hash():
    genre4 = Genre("Horror")
    assert repr(genre4) == "<Genre Horror>"
    assert hash(genre4) == hash(genre4)

    