from datetime import datetime

from pydantic import BaseModel


class Metadata(BaseModel):
    """Author's metadata structure."""

    name: str | None = None
    birth_date: datetime | None = None
    died_at: datetime | None = None


class Nationality(BaseModel):
    """Author's nationality structure."""

    id: str | None = None
    label: str
    slug: str | None = None


class AuthorRaw(BaseModel):
    """Author's raw schema."""

    metadata: Metadata
    nationalities: list[Nationality] = []


class BookRaw(BaseModel):
    """Book's raw schema."""

    name: str
    pages: int
    author: str
    publisher: str


class Content(BaseModel):
    """Review's content structure."""

    text: str


class Rating(BaseModel):
    """Review's rating structure."""

    rate: int
    label: str


class BookReviewItemMetadata(BaseModel):
    """BookReviewItem's metadata structure."""

    title: str
    pages: str


class BookReviewItem(BaseModel):
    """Structure for items in `books` list field in `ReviewRaw`."""

    id: str | None = None
    metadata: BookReviewItemMetadata


class MovieReviewItem(BaseModel):
    """Structure for items in `movies` list field in `ReviewRaw`."""

    id: int
    title: str


class ReviewRaw(BaseModel):
    """Review's raw schema."""

    content: Content
    rating: Rating
    books: list[BookReviewItem]
    movies: list[MovieReviewItem]
