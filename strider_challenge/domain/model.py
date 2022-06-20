from datetime import datetime
from hashlib import sha1
from typing import Any

from sqlmodel import Field, SQLModel

from strider_challenge.domain import raw


class Author(SQLModel, table=True):
    name: str = Field(primary_key=True)
    birth_date: datetime
    died_at: datetime | None = None
    nationality: str


def build_author(author_raw: raw.AuthorRaw) -> Author | None:
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
    title: str = Field(primary_key=True)
    pages: int
    author: str
    publisher: str


def build_book(book_raw: raw.BookRaw) -> Book:
    return Book(
        title=book_raw.name,
        pages=book_raw.pages,
        author=book_raw.author,
        publisher=book_raw.publisher,
    )


class Review(SQLModel, table=True):
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
    email: str = Field(primary_key=True)
    first_name: str
    last_name: str


class Movie(SQLModel, table=True):
    title: str = Field(primary_key=True)
    duration_mins: int
    original_language: str
    size_mb: int


class Stream(SQLModel, table=True):
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
