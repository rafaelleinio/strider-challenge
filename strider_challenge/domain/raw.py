from datetime import datetime

from pydantic import BaseModel


class Metadata(BaseModel):
    name: str | None = None
    birth_date: datetime | None = None
    died_at: datetime | None = None


class Nationality(BaseModel):
    id: str | None = None
    label: str
    slug: str | None = None


class AuthorRaw(BaseModel):
    metadata: Metadata
    nationalities: list[Nationality] = []


class BookRaw(BaseModel):
    name: str
    pages: int
    author: str
    publisher: str


class Content(BaseModel):
    text: str


class Rating(BaseModel):
    rate: int
    label: str


class BookReviewItemMetadata(BaseModel):
    title: str
    pages: str


class BookReviewItem(BaseModel):
    id: str | None = None
    metadata: BookReviewItemMetadata


class MovieReviewItem(BaseModel):
    id: int
    title: str


class ReviewRaw(BaseModel):
    content: Content
    rating: Rating
    books: list[BookReviewItem]
    movies: list[MovieReviewItem]
