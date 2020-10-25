import pytest

from covid.domain.model import Director

@pytest.fixture
def director():
    return Director("Taika Waititi")

def test_director(director):
    assert repr(director) == "<Director Taika Waititi>"

def test_init():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"

def test_if_director_none():
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None

def test_director_same():
    director1 = Director("Taika Waititi")
    assert director1 == director1

def test_director_different():
    director1 = Director("Taika Waititi")
    director4 = Director("Harry Potter")
    assert director1 != director4
   
def test_director_above():
    director1 = Director("Taika Waititi")
    director4 = Director("Harry Potter")
    assert director4 < director1
    
def test_director_hash():
    director4 = Director("Harry Potter")
    assert hash(director4) == hash(director4)