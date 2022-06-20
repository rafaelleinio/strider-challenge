from datetime import datetime
from hashlib import sha1
from typing import Any

from sqlmodel import Field, SQLModel

from strider_challenge.domain import raw


class Author(SQLModel, table=True):
    """Domain's author model.

    Two different authors don’t use the same name to publish books.

    Attributes:
        name: author's name.
        birth_date: birth date.
        died_at: date of death.
        nationality: the status of belonging to a particular nation.

    """

    name: str = Field(primary_key=True)
    birth_date: datetime
    died_at: datetime | None = None
    nationality: str


def build_author(author_raw: raw.AuthorRaw) -> Author | None:
    """Transform Author's raw record into the main model.

    Args:
        author_raw: raw record.

    Returns:
        modeled record.

    """
    name = author_raw.metadata.name
    if name:
        return Author(
            name=name,
            birth_date=author_raw.metadata.birth_date,
            died_at=author_raw.metadata.died_at,
            nationality=[
                n.slug for n in author_raw.nationalities if n.slug not in ["", None]
            ].pop(),
        )
    return None


class Book(SQLModel, table=True):
    """Domain's book model.

    Two different books can’t be published using the exact same title.

    Attributes:
        title: book's title (name).
        pages: how many pages the book have.
        author: name of the author that wrote the book.
        publisher: name of the publisher that published the book.

    """

    title: str = Field(primary_key=True)
    pages: int
    author: str
    publisher: str


def build_book(book_raw: raw.BookRaw) -> Book:
    """Transform Book's raw record into the main model.

    Args:
        book_raw: raw record.

    Returns:
        modeled record.

    """
    return Book(
        title=book_raw.name,
        pages=book_raw.pages,
        author=book_raw.author,
        publisher=book_raw.publisher,
    )


class Review(SQLModel, table=True):
    """Domain's review model.

    There are only reviews for movies based on books.

    Attributes:
        id: unique reference to a review event. Automatically generated hashing the
            text, rating, and movie_title attributes.
        text: text of the review.
        rating: score given in the review (integer number between 1 and 5).
        movie_title: name of the movie reviewed.
        book_title: name of the book in which the movie was based.

    """

    id: str = Field(primary_key=True, default=None)
    text: str
    rating: int
    movie_title: str
    book_title: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.id = sha1(
            f"{self.text}{self.rating}{self.movie_title}".encode("utf-8")
        ).hexdigest()


def build_review(review_raw: raw.ReviewRaw) -> Review:
    """Transform Review's raw record into the main model.

    Args:
        review_raw: raw record.

    Returns:
        modeled record.

    """
    return Review(
        text=review_raw.content.text,
        rating=review_raw.rating.rate,
        movie_title=[
            movie.title
            for movie in review_raw.movies
            if movie.title not in [None, "", "end"]
        ].pop(),
        book_title=[book.metadata.title for book in review_raw.books][:1].pop(),
    )


class User(SQLModel, table=True):
    """Domain's user model.

    Users' emails are verified and unique in the database

    Attributes:
        emailt: user's email.
        first_name: first name.
        last_name: last name.

    """

    email: str = Field(primary_key=True)
    first_name: str
    last_name: str


class Movie(SQLModel, table=True):
    """Domain's movie model.

    Attributes:
        title: movie's title (name).
        duration_mins: duration in minutes.
        original_language: original language in which the movie was done.
        size_mb: size of the movie file in megabytes.

    """

    title: str = Field(primary_key=True)
    duration_mins: int
    original_language: str
    size_mb: int


class Stream(SQLModel, table=True):
    """Domain's stream model.

    Attributes:
        id: unique reference to a stream event. Automatically generated hashing the
            movie_title, user_email, start_at, and end_at attributes.
        movie_title: title of the movie watched in the stream.
        user_email: email for the user that watched the stream.
        size_mb: size of the stream in megabytes.
        start_at: start time of the stream.
        end_at: end time of the stream.

    """

    id: str = Field(primary_key=True, default=None)
    movie_title: str
    user_email: str
    size_mb: str
    start_at: datetime
    end_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.id = sha1(
            f"{self.movie_title}{self.user_email}{self.start_at}{self.end_at}".encode(
                "utf-8"
            )
        ).hexdigest()
