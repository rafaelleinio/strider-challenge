from typing import Type

from sqlmodel import Session, SQLModel

from strider_challenge import adapters
from strider_challenge.adapters import SqlRepository
from strider_challenge.domain import model, raw


def _build_repo(
    model_: Type[SQLModel],
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> adapters.AbstractRepository:
    if repo:
        return repo
    if session:
        return SqlRepository(model=model_, session=session)
    raise ValueError("Both repo and session cannot be None, one must be set.")


def load_movies(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> None:
    """Extract, transform, and load records into Movie model repository.

    Args:
        collector: how to extract the records.
        repo: where to load the records.
        session: session to be used in repository.

    """
    movies = [model.Movie(**record) for record in collector.collect()]
    _build_repo(model.Movie, repo, session).add(records=movies)


def load_streams(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> None:
    """Extract, transform, and load records into Stream model repository.

    Args:
        collector: how to extract the records.
        repo: where to load the records.
        session: session to be used in repository.

    """
    streams = [model.Stream(**record) for record in collector.collect()]
    _build_repo(model.Stream, repo, session).add(records=streams)


def load_users(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> None:
    """Extract, transform, and load records into User model repository.

    Args:
        collector: how to extract the records.
        repo: where to load the records.
        session: session to be used in repository.

    """
    users = [model.User(**record) for record in collector.collect()]
    _build_repo(model.User, repo, session).add(records=users)


def load_authors(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> None:
    """Extract, transform, and load records into Author model repository.

    This service filters out malformed records, like the ones with null values in name.

    Args:
        collector: how to extract the records.
        repo: where to load the records.
        session: session to be used in repository.

    """
    authors_raw = [raw.AuthorRaw(**record) for record in collector.collect()]
    authors = [
        author
        for author in [model.build_author(author_raw) for author_raw in authors_raw]
        if author
    ]
    _build_repo(model.Author, repo, session).add(records=authors)


def load_books(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> None:
    """Extract, transform, and load records into Book model repository.

    Args:
        collector: how to extract the records.
        repo: where to load the records.
        session: session to be used in repository.

    """
    books_raw = [raw.BookRaw(**record) for record in collector.collect()]
    books = [model.build_book(book_raw) for book_raw in books_raw]
    _build_repo(model.Book, repo, session).add(records=books)


def load_reviews(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
    session: Session | None = None,
) -> None:
    """Extract, transform, and load records into Review model repository.

    Args:
        collector: how to extract the records.
        repo: where to load the records.
        session: session to be used in repository.

    """
    reviews_raw = [raw.ReviewRaw(**record) for record in collector.collect()]
    reviews = [model.build_review(review_raw) for review_raw in reviews_raw]
    _build_repo(model.Review, repo, session).add(records=reviews)
