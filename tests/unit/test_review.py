import pytest
import time

from covid.domain.model import Review, Movie

def test_review(review1):
    movie1 = Movie(0, "Harry Potter", 2010)
    review1 = Review(movie1, "amazing", 10)
    assert review1.review_text == "amazing"
    assert review1.rating == 10
    assert review1.movie == movie1

def test_review_different():
    movie1 = Movie(0, "Harry Potter", 2010)
    review1 = Review(movie1, "amazing", 10)
    time.sleep(1)
    movie2 = Movie(1, "Harry Potter", 2010)
    review2 = Review(movie2, "amazing", 10)
    assert review1 != review2

def test_review_max():
    movie2 = Movie(0, "Harry Potter", 2010)
    review3 = Review(movie2, "amazing", 50)
    assert review3.rating == None
    