# strider-challenge

## How to use?

### Testing the CLI on docker compose
Build and create all infrastructure:
```bash
make app
```

Now inside container... 

Create all model tables:
```bash
scli init-db
```

Run load commands to populate the tables:
```bash
# internal data
scli load --model movie --collector csv --config data/internal/movies.csv
scli load --model stream --collector csv --config data/internal/streams.csv
scli load --model user --collector csv --config data/internal/users.csv

# vendor data
scli load --model author --collector json --config data/vendor/authors.json
scli load --model book --collector json --config data/vendor/books.json
scli load --model review --collector json --config data/vendor/reviews.json
```

All done! 🚀

Now in your favorite DB IDE (without closing the previous process), you can connect to 
`postgresql://postgres:postgres@db:5432/dw` and query the models.

## Analytical queries over test data:
> _**Disclaimer**: for productive environments, some queries (if they need to run regularly)_ 
> _would benefit from templating input values (like timestamps)_
> 
#### What percentage of the streamed movies are based on books?
```sql
with movies_based_on_books as (
    select distinct
        movie.title as movie_title
    from
        movie
        join review
            on lower(movie.title) = lower(review.movie_title)
),
streamed_movies as (
    select distinct
        movie.title as movie_title
    from
        movie
        join stream
            on movie.title = stream.movie_title
),
counts as (
    select
        count(streamed_movies.movie_title) as count_streamed_movies,
        count(movies_based_on_books.movie_title) as count_streamed_movies_based_on_books
    from
        streamed_movies
        left join movies_based_on_books
            on streamed_movies.movie_title = movies_based_on_books.movie_title
)
select
    round(count_streamed_movies_based_on_books::numeric / count_streamed_movies::numeric, 2)
        as percentage_of_streamed_movies_based_on_books
from
    counts
```
| percentage\_of\_streamed\_movies\_based\_on\_books |
| :--- |
| 0.93 |


#### During Christmas morning (7 am and 12 noon on December 25), a partial system outage was caused by a corrupted file. Knowing the file was part of the movie "Unforgiven" thus could affect any in-progress streaming session of that movie, how many users were potentially affected?
```sql
with streams_during_christmas_morning as (
    select
        movie_title,
        user_email
    from
        stream
    where
        start_at between
            '2021-12-25T07:00:00.000+0100'::timestamp
            and '2021-12-25T12:00:00.000+0100'::timestamp
        or end_at between
            '2021-12-25T07:00:00.000+0100'::timestamp
            and '2021-12-25T12:00:00.000+0100'::timestamp
),
unforgiven_streams as (
    select distinct
        user_email
    from
        streams_during_christmas_morning
    where
        lower(movie_title) = 'unforgiven'
)
select
    count(user_email) as count_users_affected
from
    unforgiven_streams

```
| count\_users\_affected |
| :--- |
| 5 |


#### How many movies based on books written by Singaporeans authors were streamed that month?
```sql
with singaporean_authors as (
    select
        name
    from
        author
    where
        nationality = 'singaporeans'
),
books_from_sing_authors as (
    select
        book.title,
        book.author
    from
        book
        join singaporean_authors
            on lower(book.author) = lower(singaporean_authors.name)
),
movies_based_on_books as (
    select distinct
        movie.title as movie_title,
        review.book_title
    from
        movie
        join review
            on lower(movie.title) = lower(review.movie_title)
),
movies_streamed_in_december as (
    select distinct
        movie_title
    from
        stream
    where
        start_at between
            '2021-12-01T00:00:00.000+0100'::timestamp
            and '2021-12-31T23:59:59.000+0100'::timestamp
        or end_at between
            '2021-12-01T00:00:00.000+0100'::timestamp
            and '2021-12-31T23:59:59.000+0100'::timestamp
),
movies_based_on_books_from_sing_authors as (
    select distinct
        movie_title
    from
        books_from_sing_authors
        join movies_based_on_books on
            lower(books_from_sing_authors.title) = lower(movies_based_on_books.book_title)
)
select
    count(1) as result
from
    movies_based_on_books_from_sing_authors
    join movies_streamed_in_december
        on lower(movies_based_on_books_from_sing_authors.movie_title) =  lower(movies_streamed_in_december.movie_title)
```
| result |
| :--- |
| 3 |


#### What's the average streaming duration?
```sql
select
    avg(EXTRACT(EPOCH FROM (end_at - start_at)))::int as "avg stream duration (seconds)"
from
    stream
```
| avg stream duration \(seconds\) |
| :--- |
| 43336 |


#### What's the **median** streaming size in gigabytes?
```sql
select
    round((percentile_cont(0.5) within group (order by size_mb::numeric) / 1000)::numeric, 2) as median_size_in_gb
from
    stream
```
| median\_size\_in\_gb |
| :--- |
| 0.94 |


#### Given the stream duration (start and end time) and the movie duration, how many users watched at least 50% of any movie in the last week of the month (7 days)?
> assuming _the month_ here refers to December 2021 🤔
```sql
with streams_december_last_week as (
    select
        *
    from
        stream
    where
        start_at between
            '2021-12-24T00:00:00.000+0100'::timestamp
            and '2021-12-31T23:59:59.000+0100'::timestamp
        or end_at between
            '2021-12-24T00:00:00.000+0100'::timestamp
            and '2021-12-31T23:59:59.000+0100'::timestamp
),
stream_durations as (
    select
        EXTRACT(EPOCH FROM (end_at - start_at))/60 stream_duration_minutes,
        movie.duration_mins as movie_durantion_mins,
        streams_december_last_week.user_email
    from
        streams_december_last_week
        join movie
            on lower(streams_december_last_week.movie_title) = lower(movie.title)
),
over_half_duration as (
    select
        *,
        stream_duration_minutes >= (movie_durantion_mins * 0.5) as is_over_half
    from
        stream_durations
),
users_over_half_duration as (
    select distinct
        user_email
    from
        over_half_duration
    where
        is_over_half
)
select
    count(user_email) as result
from
    users_over_half_duration
```
| result |
| :--- |
| 746 |
