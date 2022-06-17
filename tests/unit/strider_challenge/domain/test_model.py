import datetime

from strider_challenge.domain import model


def test_build_author():
    # arrange
    author_raw = model.raw.AuthorRaw(
        metadata=model.raw.Metadata(
            name="name",
            birth_date=datetime.datetime(2000, 1, 1),
            died_at=datetime.datetime(2022, 1, 1),
        ),
        nationalities=[
            model.raw.Nationality(
                label="Guianese (French)",
                slug="guianese-french",
            ),
            model.raw.Nationality(
                label="",
            ),
        ],
    )
    target_author = model.Author(
        name="name",
        birth_date=datetime.datetime(2000, 1, 1),
        died_at=datetime.datetime(2022, 1, 1),
        nationalities=["guianese-french"],
    )

    # act
    output_author = model.build_author(author_raw=author_raw)

    # assert
    assert output_author == target_author


def test_build_book():
    # arrange
    book_raw = model.raw.BookRaw(
        name="title",
        pages=123,
        author="author",
        publisher="publisher",
    )
    target_book = model.Book(
        title="title",
        pages=123,
        author="author",
        publisher="publisher",
    )

    # act
    output_book = model.build_book(book_raw=book_raw)

    # assert
    assert output_book == target_book


def test_build_review():
    # arrange
    review_raw = model.raw.ReviewRaw(
        content=model.raw.Content(text="text"),
        rating=model.raw.Rating(
            rate=5,
            label="FIVE",
        ),
        books=[
            model.raw.BookReviewItem(
                metadata=model.raw.BookReviewItemMetadata(
                    title="book_title",
                    pages="pages",
                )
            )
        ],
        movies=[
            model.raw.MovieReviewItem(
                id=0,
                title="movie_title",
            ),
            model.raw.MovieReviewItem(
                id=0,
                title="end",
            ),
        ],
    )
    target_review = model.Review(
        text="text", rating=5, movie_title="movie_title", book_title="book_title"
    )

    # act
    output_review = model.build_review(review_raw=review_raw)

    # assert
    assert output_review == target_review


def test_stream_id_generation():
    # act
    stream = model.Stream(
        movie_title="title",
        user_email="email",
        size_mb=256,
        start_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    # act and assert
    assert stream.id == "1916a9ad445f73d0b20638309ae1fad9fec452df"
