from strider_challenge import adapters
from strider_challenge.domain import model, raw


def load_movies(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository,
) -> None:
    movies = [model.Movie(**record) for record in collector.collect()]
    repo.add(records=movies)


def load_streams(
    collector: adapters.Collector, repo: adapters.AbstractRepository
) -> None:
    streams = [model.Stream(**record) for record in collector.collect()]
    repo.add(records=streams)


def load_users(
    collector: adapters.Collector, repo: adapters.AbstractRepository
) -> None:
    users = [model.User(**record) for record in collector.collect()]
    repo.add(records=users)


def load_authors(
    collector: adapters.Collector, repo: adapters.AbstractRepository
) -> None:
    authors_raw = [raw.AuthorRaw(**record) for record in collector.collect()]
    authors = [
        author
        for author in [model.build_author(author_raw) for author_raw in authors_raw]
        if author
    ]
    repo.add(records=authors)


def load_books(
    collector: adapters.Collector, repo: adapters.AbstractRepository
) -> None:
    books_raw = [raw.BookRaw(**record) for record in collector.collect()]
    books = [model.build_book(book_raw) for book_raw in books_raw]
    repo.add(records=books)


def load_reviews(
    collector: adapters.Collector, repo: adapters.AbstractRepository
) -> None:
    reviews_raw = [raw.ReviewRaw(**record) for record in collector.collect()]
    reviews = [model.build_review(review_raw) for review_raw in reviews_raw]
    repo.add(records=reviews)
