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
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None

    