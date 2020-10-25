from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import covid.adapters.repository as repo
import covid.utilities.utilities as utilities
import covid.news.services as services

from covid.authentication.authentication import login_required


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)

@movies_blueprint.route('/', methods=['GET'])
#@movies_blueprint.route('/movies_by_year', methods=['GET'])
def movies_by_year():
    # Read query parameters.
    target_year = request.args.get('year')
    # article_to_show_comments = request.args.get('view_comments_for') #make reviews?

    ordered_movies = services.get_sorted_movies_by_year(target_year, repo.repo_instance) # You need to make this

    # Fetch the first and last articles in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_year is None:
        # No date query parameter, so return articles from day 1 of the series.
        #target_year = first_movie['year']
        target_year = first_movie['year']
    else:
        # Convert target_date from string to date.
        target_year = date.fromisoformat(target_year)

    #if article_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent article id.
        #article_to_show_comments = -1
    #else:
        # Convert article_to_show_comments from string to int.
        #article_to_show_comments = int(article_to_show_comments)

    # Fetch article(s) for the target date. This call also returns the previous and next dates for articles immediately
    # before and after the target date.
    movies_by_year, previous_year, next_year = services.get_sorted_movies_by_year(target_year, repo.repo_instance)

    first_year_url = None
    last_year_url = None
    next_year_url = None
    prev_year_url = None

    if len(movies_by_year) > 0:
        # There's at least one article for the target date.
        if previous_year is not None:
            # There are articles on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_year_url = url_for('movies_bp.movies_by_year', year = previous_year.isoformat())
            #first_movie_url = url_for('movies_bp.movies_by_year', year=first_movie['year'].isoformat())
            first_year_url = url_for('movies_bp.movies_by_year', year = first_movie['year'].isoformat())

        # There are articles on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_year is not None:
            next_year_url = url_for('movies_bp.movies_by_year', year = next_year)
            #last_movie_url = url_for('movies_bp.movies_by_year', year=last_movie['year'].isoformat())
            last_year_url = url_for('movies_bp.movies_by_year', year = last_movie['year'])

        # Construct urls for viewing article comments and adding comments.
        #for article in articles:
        #    article['view_comment_url'] = url_for('movies_bp.movies_by_year', date=target_date, view_comments_for=article['id'])
        #    article['add_comment_url'] = url_for('movies_bp.comment_on_article', article=article['id'])

        # Generate the webpage to display the articles.
        #return render_template(
        #    'news/articles.html',
        #    title='Movies',
        #    articles_title=target_date.strftime('%A %B %e %Y'),
        #    articles=articles,
        #    selected_articles=utilities.get_selected_articles(len(articles) * 2),
        #    tag_urls=utilities.get_tags_and_urls(),
        #    first_article_url=first_article_url,
        #    last_article_url=last_article_url,
        #    prev_article_url=prev_article_url,
        #    next_article_url=next_article_url,
        #    show_comments_for_article=article_to_show_comments
        #)
        return render_template(
            'movies/movies.html', 
            title = "Movies",
            movies = movies_by_year,
            first_movies_url = first_year_url,
            last_movies_url = last_year_url,
            prev_movies_url = prev_year_url,
            next_movies_url = next_year_url,
        ) 

    # No articles to show, so return the homepage.
    return redirect(url_for('movies_bp.movies_by_year')) # This is so you redirect back to home if there are no movies for that year

@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    articles_per_page = 3

    # Read query parameters.
    tag_name = request.args.get('tag')
    cursor = request.args.get('cursor')
    article_to_show_comments = request.args.get('view_comments_for')

    if article_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent article id.
        article_to_show_comments = -1
    else:
        # Convert article_to_show_comments from string to int.
        article_to_show_comments = int(article_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    article_ids = services.get_article_ids_for_tag(tag_name, repo.repo_instance)

    # Retrieve the batch of articles to display on the Web page.
    articles = services.get_articles_by_id(article_ids[cursor:cursor + articles_per_page], repo.repo_instance)

    first_article_url = None
    last_article_url = None
    next_article_url = None
    prev_article_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_article_url = url_for('movies_bp.movies_by_genre', tag=tag_name, cursor=cursor - articles_per_page)
        first_article_url = url_for('movies_bp.movies_by_genre', tag=tag_name)

    if cursor + articles_per_page < len(article_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_article_url = url_for('movies_bp.movies_by_genre', tag=tag_name, cursor=cursor + articles_per_page)

        last_cursor = articles_per_page * int(len(article_ids) / articles_per_page)
        if len(article_ids) % articles_per_page == 0:
            last_cursor -= articles_per_page
        last_article_url = url_for('movies_bp.movies_by_genre', tag=tag_name, cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    for article in articles:
        article['view_comment_url'] = url_for('movies_bp.movies_by_genre', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
        article['add_comment_url'] = url_for('movies_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movies.html',
        title='Articles',
        articles_title='Articles tagged by ' + tag_name,
        articles=articles,
        selected_articles=utilities.get_selected_articles(len(articles) * 2),
        tag_urls=utilities.get_tags_and_urls(),
        first_article_url=first_article_url,
        last_article_url=last_article_url,
        prev_article_url=prev_article_url,
        next_article_url=next_article_url,
        show_comments_for_article=article_to_show_comments
    )


@movies_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_article():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        article_id = int(form.article_id.data)

        # Use the service layer to store the new comment.
        services.add_comment(article_id, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        article = services.get_article(article_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.movies_by_year', date=article['date'], view_comments_for=article_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        article_id = int(request.args.get('article'))

        # Store the article id in the form.
        form.article_id.data = article_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        article_id = int(form.article_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    article = services.get_article(article_id, repo.repo_instance)
    return render_template(
        'movies/comment_on_article.html',
        title='Edit article',
        article=article,
        form=form,
        handler_url=url_for('movies_bp.comment_on_article'),
        selected_articles=utilities.get_selected_articles(),
        tag_urls=utilities.get_tags_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    article_id = HiddenField("Article id")
    submit = SubmitField('Submit')