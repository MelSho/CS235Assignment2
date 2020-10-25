import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from covid.adapters.repository import AbstractRepository, RepositoryException
from covid.domain.model import Article, Tag, User, Comment, make_tag_association, make_comment, Movie, Director, Actor, Genre



class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._articles = list()
        self._articles_index = dict()
        self._tags = list()
        self._users = list()
        self._comments = list()
        self._movies = list()
        self._movies_index = dict()
        self._actors = list()
        self._directors = list()
        self._genres = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_article(self, article: Article):
        insort_left(self._articles, article)
        self._articles_index[article.id] = article

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.rank] = movie

    def get_article(self, id: int) -> Article:
        article = None

        try:
            article = self._articles_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return article

    def get_movie(self, rank: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[rank]
        except KeyError:
            pass
        return movie

    def get_sorted_movies_by_year(self, target_year: int) ->List[Movie]:
        target_movie = Movie(
            rank = None,
            title = None,
            year = target_year
        )
        matching_movies = list()

        try:
            index = self.movie_index(target_movie)
            for movie in self._movies[index:None]:
                if movie.year == target_year:
                    matching_movies.append(movie)
                else:
                    break
        except ValueError:
            pass
        return matching_movies

    def get_articles_by_date(self, target_date: date) -> List[Article]:
        target_article = Article(
            date=target_date,
            title=None,
            first_para=None,
            hyperlink=None,
            image_hyperlink=None
        )
        matching_articles = list()

        try:
            index = self.article_index(target_article)
            for article in self._articles[index:None]:
                if article.date == target_date:
                    matching_articles.append(article)
                else:
                    break
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass

        return matching_articles

    def get_number_of_movies(self):
        return len(self._movies)

    def get_number_of_articles(self):
        return len(self._articles)

    def get_first_movie(self):
        movie = None
        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_first_article(self):
        article = None

        if len(self._articles) > 0:
            article = self._articles[0]
        return article

    def get_last_movie(self):
        movie = None
        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_last_article(self):
        article = None

        if len(self._articles) > 0:
            article = self._articles[-1]
        return article

    def get_articles_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self._articles_index]

        # Fetch the Articles.
        articles = [self._articles_index[id] for id in existing_ids]
        return articles
    
    def get_movies_by_rank(self, rank_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ranks = [id for id in rank_list if id in self._movies_index]

        # Fetch the Articles.
        movies = [self._movies_index[id] for id in existing_ranks]
        return movies

    def get_article_ids_for_tag(self, tag_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self._tags if tag.tag_name == tag_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            article_ids = [article.id for article in tag.tagged_articles]
        else:
            # No Tag with name tag_name, so return an empty list.
            article_ids = list()

        return article_ids
    
    def get_movie_ranks_for_genre(self, genre_name: str):
        # iterate movies, if genre same put in list
        movie_ranks = list()
        for movie in self._movies:
            if genre_name in movie.genres:
                movie_ranks.append(movie.rank)
        return movie_ranks
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        #genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of articles associated with the Tag.
        #if genre is not None:
        #    movie_ranks = [movie.rank for movie in genre.genreList]
        #else:
            # No Tag with name tag_name, so return an empty list.
        #    movie_ranks = list()

        #return movie_ranks

    def get_year_of_previous_movie(self, movie: Movie):
        previous_year = None
        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.year < movie.year:
                    previous_year = stored_movie.year
                    break
        except ValueError:
            pass
        return previous_year

    def get_date_of_previous_article(self, article: Article):
        previous_date = None

        try:
            index = self.article_index(article)
            for stored_article in reversed(self._articles[0:index]):
                if stored_article.date < article.date:
                    previous_date = stored_article.date
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_date

    def get_year_of_next_movie(self, movie: Movie):
        next_year = None
        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.year > movie.year:
                    next_year = stored_movie.year
                    break
        except ValueError:
            pass
        return next_year

    def get_date_of_next_article(self, article: Article):
        next_date = None

        try:
            index = self.article_index(article)
            for stored_article in self._articles[index + 1:len(self._articles)]:
                if stored_article.date > article.date:
                    next_date = stored_article.date
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def add_tag(self, tag: Tag):
        self._tags.append(tag)

    def get_tags(self) -> List[Tag]:
        return self._tags

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        self._comments.append(comment)

    def get_comments(self):
        return self._comments

    # Helper method to return article index.
    def article_index(self, article: Article):
        index = bisect_left(self._articles, article)
        if index != len(self._articles) and self._articles[index].date == article.date:
            return index
        raise ValueError

    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].year == movie.year:
            return index
        raise ValueError
    
    def add_actor(self, actor: Actor):
        self._actors.append(actor)
    
    def add_director(self, director: Director):
        self._directors.append(director)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_movies(data_path: str, repo: MemoryRepository):
    dataset_of_movies: list = []
    dataset_of_actors: set = set()
    dataset_of_directors: set = set()
    dataset_of_genres: set = set()

    index = 0
    for row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        rank = row[0]
        title = row[1]
        year = int(row[6])
        movie = Movie(rank, title, year)
        dataset_of_movies.append(movie)
        repo.add_movie(movie) #
        actors = row[5]
        actors = actors.split(",")
        for x in range(0, len(actors)):
            actors[x] = actors[x].strip()
            if (actors[x] not in dataset_of_actors):
                actor = Actor(actors[x])
                dataset_of_actors.add(actor)
                repo.add_actor(actor) #
        directors = row[4]
        if (directors not in dataset_of_directors):
            director = Director(directors)
            dataset_of_directors.add(director)
            repo.add_director(director) #
        genres = row[2]
        genres = genres.split(",")
        for x in range(0, len(genres)):
            genres[x] = genres[x].strip()
            if (genres[x] not in dataset_of_genres):
                genre = Genre(genres[x])
                dataset_of_genres.add(genre)
                repo.add_genre(genre) #
        #print(f"Movie {index} with title: {title}, release year {release_year}")
        index += 1

        movie = Movie(
            rank = row[0],
            title = row[1],
            year = int(row[6])
        )

        repo.add_movie(movie)

def load_articles_and_tags(data_path: str, repo: MemoryRepository):
    tags = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'news_articles.csv')):

        article_key = int(data_row[0])
        number_of_tags = len(data_row) - 6
        article_tags = data_row[-number_of_tags:]

        # Add any new tags; associate the current article with tags.
        for tag in article_tags:
            if tag not in tags.keys():
                tags[tag] = list()
            tags[tag].append(article_key)
        del data_row[-number_of_tags:]

        # Create Article object.
        article = Article(
            date=date.fromisoformat(data_row[1]),
            title=data_row[2],
            first_para=data_row[3],
            hyperlink=data_row[4],
            image_hyperlink=data_row[5],
            id=article_key
        )

        # Add the Article to the repository.
        repo.add_article(article)

    # Create Tag objects, associate them with Articles and add them to the repository.
    for tag_name in tags.keys():
        tag = Tag(tag_name)
        for article_id in tags[tag_name]:
            article = repo.get_article(article_id)
            make_tag_association(article, tag)
        repo.add_tag(tag)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            article=repo.get_article(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_articles_and_tags(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)

    # Load movies into the repository. 
    load_movies(data_path, repo)