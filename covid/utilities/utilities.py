from flask import Blueprint, request, render_template, redirect, url_for, session

import covid.adapters.repository as repo
import covid.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_tags_and_urls():
    tag_names = services.get_tag_names(repo.repo_instance)
    tag_urls = dict()
    for tag_name in tag_names:
        tag_urls[tag_name] = url_for('movies_bp.movies_by_genre', tag=tag_name)

    return tag_urls

def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_selected_articles(quantity=3):
    articles = services.get_random_articles(quantity, repo.repo_instance)

    for article in articles:
        article['hyperlink'] = url_for('movies_bp.movies_by_year', date=article['date'].isoformat())
    return articles

def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.movies_by_year', date=movie['year'])
    return movies