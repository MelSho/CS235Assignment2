from datetime import date, datetime
from typing import List, Iterable

class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
            self.__coworkers: set = set()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return other.__actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if (colleague not in self.__coworkers):
            self.__coworkers.add(colleague)
    
    def check_if_this_actor_worked_with(self, colleague):
        if (colleague not in self.__coworkers):
            return False
        return True

class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return other.__director_full_name == self.__director_full_name

    def __lt__(self, other):
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)

class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False
        return other.__genre_name == self.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)

class Movie:

    def __init__(self, rank: int, title: str, year: int, description: str, director: str, actors: list, genre: list, rating: str):
        if title == "" or title == None or type(title) is not str:
            self.__rank: None
            self.__title = None
            self.__year = None
            self.__description = None
            self.__director = None
            self.__actorList = None
            self.__genreList = None
            self.__runtime = None
        if year == "" or year == None or type(year) is not int:
            self.__rank: None
            self.__title = None
            self.__year = None
            self.__description = None
            self.__director = None
            self.__actorList = None
            self.__genreList = None
            self.__runtime = None
        else:
            self.__rank = rank
            #self.__title = title.strip()
            self.__title = title
            self.__year = year
            self.__description = description
            self.__director = director
            self.__actorList = actors
            self.__genreList = genre
            self.__rating = rating
            self.__runtime = 0
            
    @property
    def rank(self) -> str:
        return self.__rank

    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def year(self) -> int:
        return self.__year

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, descr: str):
        self.__description = descr.strip()
    
    @property
    def director(self) -> Director:
        return self.__director
    
    @director.setter
    def director(self, director1: Director):
        self.__director = director1

    @property
    def actors(self) -> list:
        return self.__actorList

    @actors.setter
    def actors(self, value: Actor):
        self.__actorList.append(value)

    @property
    def genres(self) -> list:
        return self.__genreList

    @genres.setter
    def genres(self, value: Genre):
        self.__genreList.append(value)
    
    @property
    def runtime_minutes(self) -> int:
        return self.__runtime

    @runtime_minutes.setter
    def runtime_minutes(self, value: int):
        if value < 0:
            raise ValueError
        self.__runtime = value

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__year}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Movie):
            return False
        return (other.__title == self.__title) and (other.__year == self.__year)

    def __lt__(self, other):
        if (other.__title == None):
            return False
        if (self.__title == other.__title):
            return self.__year < other.__year
        return self.__title < other.__title

    def __hash__(self):
        return hash(self.__title + str(self.__year))

    def add_actor(self, addActor: Actor):
        if (addActor not in self.__actorList):
            self.__actorList.append(addActor)

    def remove_actor(self, removeActor: Actor):
        if (removeActor in self.__actorList):
            self.__actorList.remove(removeActor)

    def add_genre(self, addGenre: Genre):
        if (addGenre not in self.__genreList):
            self.__genreList.append(addGenre)

    def remove_genre(self, removeGenre: Genre):
        if (removeGenre in self.__genreList):
            self.__genreList.remove(removeGenre)

class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int):
        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()
        if type(rating) is not int:
            self.__rating = None
        else:
            if rating > 10 or rating < 1:
                self.__rating = None
            else:
                self.__rating = rating
        if type(movie) is not Movie:
            self.__movie = None
        else:
            self.__movie = movie
        self.__timestamp = datetime.now()

    @property
    def review_text(self) -> str:
        return self.__review_text
    
    @property
    def rating(self) -> int:
        return self.__rating
    
    @property
    def movie(self) -> Movie:
        return self.__movie
    
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __repr__(self):
        return f"Review of {self.__movie} at {self.__timestamp}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return ((other.__movie == self.__movie) and (other.__review_text == self.__review_text) and (other.__rating == self.__rating) and (other.__timestamp == self.__timestamp))

class WatchList:
    def __init__(self):
        self.__WatchList = []

    @property
    def watch_list(self) -> list:
        return self.__WatchList
    
    def add_movie(self, movie: Movie):
        if (movie not in self.__WatchList):
            self.__WatchList.append(movie)
    
    def remove_movie(self, movie):
        if (movie in self.__WatchList):
            self.__WatchList.remove(movie)
    
    def select_movie_to_watch(self, index):
        if (index >= len(self.__WatchList)):
            return None
        else:
            return self.__WatchList[index]

    def size(self):
        return len(self.__WatchList)

    def first_movie_in_watchlist(self):
        if (len(self.__WatchList) == 0):
            return None
        else:
            return self.__WatchList[0]

    def __iter__(self):
        return self.__WatchList.__iter__()

    def __next__(self):
        if (len(self.__WatchList) == 0):
            raise StopIteration
        else:
            return self.__WatchList.pop(0)
            
class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._comments: List[Comment] = list()
        self.__reviews: List[Review] = list()
        self.__watched_movies = []
        self.__time_spent_watching_movies_minutes: int = 0

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self._comments)
    
    @property
    def watched_movies(self) -> list:
        return self.__watched_movies
    
    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self.__reviews)
    
    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes
    
    def __hash__(self):
        return hash(self.__username)
    
    def watch_movie(self, movie: Movie):
        if (movie not in self.__watched_movies):
            self.__watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes += movie.runtime_minutes
    
    def add_review(self, review: 'Review'):
        self.__reviews.append(review)

    def add_comment(self, comment: 'Comment'):
        self._comments.append(comment)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username

class Comment:
    def __init__(
            self, user: User, article: 'Article', comment: str, timestamp: datetime
    ):
        self._user: User = user
        self._article: Article = article
        self._comment: Comment = comment
        self._timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self._user

    @property
    def article(self) -> 'Article':
        return self._article

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other._user == self._user and other._article == self._article and other._comment == self._comment and other._timestamp == self._timestamp


class Article:
    def __init__(
            self, date: date, title: str, first_para: str, hyperlink: str, image_hyperlink: str, id: int = None
    ):
        self._id: int = id
        self._date: date = date
        self._title: str = title
        self._first_para: str = first_para
        self._hyperlink: str = hyperlink
        self._image_hyperlink: str = image_hyperlink
        self._comments: List[Comment] = list()
        self._tags: List[Tag] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def date(self) -> date:
        return self._date

    @property
    def title(self) -> str:
        return self._title

    @property
    def first_para(self) -> str:
        return self._first_para

    @property
    def hyperlink(self) -> str:
        return self._hyperlink

    @property
    def image_hyperlink(self) -> str:
        return self._image_hyperlink

    @property
    def comments(self) -> Iterable[Comment]:
        return iter(self._comments)

    @property
    def number_of_comments(self) -> int:
        return len(self._comments)

    @property
    def number_of_tags(self) -> int:
        return len(self._tags)

    @property
    def tags(self) -> Iterable['Tag']:
        return iter(self._tags)

    def is_tagged_by(self, tag: 'Tag'):
        return tag in self._tags

    def is_tagged(self) -> bool:
        return len(self._tags) > 0

    def add_comment(self, comment: Comment):
        self._comments.append(comment)

    def add_tag(self, tag: 'Tag'):
        self._tags.append(tag)

    def __repr__(self):
        return f'<Article {self._date.isoformat()} {self._title}>'

    def __eq__(self, other):
        if not isinstance(other, Article):
            return False
        return (
                other._date == self._date and
                other._title == self._title and
                other._first_para == self._first_para and
                other._hyperlink == self._hyperlink and
                other._image_hyperlink == self._image_hyperlink
        )

    def __lt__(self, other):
        return self._date < other._date


class Tag:
    def __init__(
            self, tag_name: str
    ):
        self._tag_name: str = tag_name
        self._tagged_articles: List[Article] = list()

    @property
    def tag_name(self) -> str:
        return self._tag_name

    @property
    def tagged_articles(self) -> Iterable[Article]:
        return iter(self._tagged_articles)

    @property
    def number_of_tagged_articles(self) -> int:
        return len(self._tagged_articles)

    def is_applied_to(self, article: Article) -> bool:
        return article in self._tagged_articles

    def add_article(self, article: Article):
        self._tagged_articles.append(article)

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return other._tag_name == self._tag_name

class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, article: Article, timestamp: datetime = datetime.today()):
    comment = Comment(user, article, comment_text, timestamp)
    user.add_comment(comment)
    article.add_comment(comment)

    return comment


def make_tag_association(article: Article, tag: Tag):
    if tag.is_applied_to(article):
        raise ModelException(f'Tag {tag.tag_name} already applied to Article "{article.title}"')

    article.add_tag(tag)
    tag.add_article(article)
