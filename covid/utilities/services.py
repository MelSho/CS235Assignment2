from typing import Iterable
import random

from covid.adapters.repository import AbstractRepository
from covid.domain.model import Article, Movie


def get_tag_names(repo: AbstractRepository):
    tags = repo.get_tags()
    tag_names = [tag.tag_name for tag in tags]

    return tag_names

def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_articles(quantity, repo: AbstractRepository):
    article_count = repo.get_number_of_articles()

    if quantity >= article_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = article_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, article_count), quantity)
    articles = repo.get_articles_by_id(random_ids)

    return articles_to_dict(articles)

def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_articles()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ranks = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_rank(random_ranks)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def article_to_dict(article: Article):
    article_dict = {
        'date': article.date,
        'title': article.title,
        'image_hyperlink': article.image_hyperlink
    }
    return article_dict


def articles_to_dict(articles: Iterable[Article]):
    return [article_to_dict(article) for article in articles]

def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'year': movie.year
    }
    return movie_dict

def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
