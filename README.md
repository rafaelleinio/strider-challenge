# strider-challenge
_a nice typer and sqlmodel application developed with DDD and TDD._

![Python Version](https://img.shields.io/badge/python-3.10-brightgreen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![flake8](https://img.shields.io/badge/code%20quality-flake8-blue)](https://github.com/PyCQA/flake8)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pytest coverage: 100%](https://img.shields.io/badge/pytest%20coverage-100%25-green)](https://github.com/pytest-dev/pytest)

## Context
The case definition can be reviewed [here](case.md).

### ⚠️ Attention point
While one could solve this challenge with a single ETL script and invest all the time in
designing a super fancy architecture and showing tons of cloud solutions and 
technologies in several diagrams, I preferred to take another route 🤓. I invested a lot
of time in software engineering practices and implemented this solution as a flexible, 
organized, clean, and tested codebase. Specific technologies and cloud solutions should 
be minor decisions, and the real scalability relies upon building a robust software 
layer for the data platform. Core domain business logic should be extensible for any 
type of deployment and, thus, should not be tied to specific technologies. Now let's get
down to business, see my solution below 👇

## Development highlights ✨
- 🧐 High code quality standards (static typing, style and language best practices) checking with `mypy`, `black`, `isort` and `flake8`.
- 🧰 Developed with Domain Driven Design (DDD) architecture pattern.
  - Same core domain logic and adapters can be re-utilized for any number of entrypoints.
- 🧪 Developed with Test Driven Development (TDD) practices.
  - First declaring the tests and after implementing the logic.
  - Everything is tested (100% coverage). Tests are organized as following:
    - unit: asserts single functions and classes logic without any external interference.
    - integration: test how different modules interact with each other and are orchestrated(service layer).
    - e2e: from an entrypoint testing end-to-end all the architecture with real database in docker compose.
- 📚 Everything is documented: all public classes and methods are documented.
- ✅ Production standards:
  - Client's interface for all services implemented in the lib in the form of a CLI entrypoint.
  - The application is dockerized
  - All useful commands are implemented in Makefile (easy to implement CI/CD pipelines)
- 🆕 Modern Python libs stack:
  - [pydantic](https://github.com/samuelcolvin/pydantic): for deserialization and data types validation.
  - [typer](https://github.com/tiangolo/typer): for the CLI development
  - [sqlmodel](https://github.com/tiangolo/sqlmodel): for ORM

### TDD Flow:
The following image shows the TDD flow for this project:
![](https://i.imgur.com/lFDTLaw.png)

- 🧪 commits are signatures and tests declaring a new functionality. Tests are failing at this point.
- ✍️ commits are the actual implementations of the functionalities. Tests are succeeding at this point.
- 🔨, 🐛, and 📚 are for refactoring, bug fix and documentation commits respectively.

## How to use?

### Local development
1) Create your virtual environment (e.g. pyenv)
```bash
pyenv virtualenv 3.10.3 strider-challenge-test 
```
2) Install the requirements
```bash
make requirements
```
3) Run the tests with coverage checking
```bash
make tests-coverage
```
4) Run the [e2e test](tests/e2e/strider_challenge/test_entrypoints/test_cli.py):
```bash
make e2e-tests
```
> **Disclaimer**: this command builds an infrastructure with [docker-compose](tests/e2e/docker-compose.yaml) for the test. It runs all commands of the CLI; initializes the database, and loads all the models inside the database.
5) Other useful commands:
```
❯ make help
Available rules:

app                 create db infra with docker compose 
apply-style         fix stylistic errors with black and isort 
build-docker        build strider_challenge image 
checks              run all code checks 
clean               clean unused artifacts 
e2e-tests           run e2e tests with infrastructure on docker compose 
integration-tests   run integration tests 
package             build strider_challenge package wheel 
quality-check       run code quality checks with flake8 
requirements        install requirements 
requirements-dev    install development requirements 
requirements-minimum install prod requirements 
style-check         run code style checks with black 
teardown            teardown all infra on docker compose 
tests-coverage      run unit and integration tests with coverage report 
type-check          run code type checks with mypy 
unit-tests          run unit tests 
version             show version 

```

### Project Structure
This project follows a lean DDD organization:
```
strider_challenge
├── __init__.py
├── __metadata__.py
├── adapters
│   ├── __init__.py
│   ├── collector.py
│   └── repository.py
├── domain
│   ├── __init__.py
│   ├── model.py
│   └── raw.py
├── entrypoints
│   ├── __init__.py
│   └── cli.py
└── service_layer.py
```


### CLI
Install the package:
```bash
pip install .
```
Now you have strider-challenge's cli available (`scli`) 🎉
```
❯ scli --help
Usage: scli [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  init-db  Initialize the database with all models declared in domain.
  load     Extract, transform, and load records into a specific model...
```
```
❯ scli init-db --help
Usage: scli init-db [OPTIONS]

  Initialize the database with all models declared in domain.

Options:
  --help  Show this message and exit.
```
```
❯ scli load --help
Usage: scli load [OPTIONS]

  Extract, transform, and load records into a specific model repository.

  Args:     model: what model to populate.     collector: what collector to
  use.     config: arg for the collector (path to file).

Options:
  --model [movie|stream|user|author|book|review]
                                  [default: ModelEnum.movie]
  --collector [csv|json]          [default: CollectorEnum.csv]
  --config PATH
  --help                          Show this message and exit.
```
### Testing the CLI on docker compose (start here)
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
> The loads are upserts, which means it will try to insert or update if the reference 
> already exists. Check the [repository](strider_challenge/adapters/repository.py) 
> module for more insights 

All done! 🚀

Now in your favorite DB IDE (without closing the previous process), you can connect to 
`postgresql://postgres:postgres@db:5432/dw` and query the models.

## Analytical queries over test data:
> _**Disclaimer**: 1) for productive environments, some queries (if they need to run regularly)_ 
> _would benefit from templating input values (like timestamps). 2) Queries developed 
> with PostgreSQL syntax._

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

## Next Steps
_What things could improve to make this project even more awesome?_

- Implement [custom data validators](https://pydantic-docs.helpmanual.io/usage/validators/) for the models according to business requirements for quality.
- Create `.github/workflows` yaml files to setup CI/CD pipelines for testing, building and deployment. Check [this example](https://github.com/rafaelleinio/pyspark-pipeline/tree/main/.github/workflows) from another project of mine. This step should be easy as most useful commands are already built in [Makefile](Makefile).
- Create CD pipeline to push the docker image to a registry like [ECR](https://aws.amazon.com/pt/ecr/) on releases.
- Implement new collectors according to new data source requirements: `S3Collector`, `FTPCollector`, `KafkaCollector` ...
- Refactor `service_layer` to possible make it more DRY
- Add new service to easily pull metrics from the CLI running a query file. Like `scli query -f my_query.sql`
- Add `CONTRIBUTING.md` file to document how to be a successful contributor to this project. See [this example](https://github.com/quintoandar/butterfree/blob/staging/CONTRIBUTING.md) that I did for another open source project.

### Deployment suggestion:
As this project implements a user interface (CLI) and it's dockerized already, deploying
this project should be very straightforward. It will also help a lot to have already 
implemented the pipeline to release the image to the ECR. This subsection comments on 
possible alternatives to deploy this application and orchestrate runs. 

#### As a cron job on Kubernetes
As you are probably already using K8s (2022 right? 🤣), one of the most straightforward 
deployment suggestions is by deploying it as a cronJob on your cluster. While this 
alternative is very simple, it leverages the easy deployment and elastic scalability 
capabilities of Kubernetes 🚀.

Check the [docs](https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/)
for reference. The following figure shows a simple schematic of this architecture:

![](https://i.imgur.com/uUqMQw6.png)

#### As a docker operator job on Airflow
Airflow (the most used orchestration framework for Data Engineers) have an easy-to-use 
operator for dockerized apps. You can use the DockerOperator to do it! Check 
[this](https://www.lucidchart.com/techblog/2019/03/22/using-apache-airflows-docker-operator-with-amazons-container-repository/)
cool reference on this subject. Example:

```python
DockerOperator(
    task_id="web_scraper",
    image="XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/strider-challenge:latest",
    command='scli load --model movie --collector s3 --config s3://my-bucket/path/to/movies.csv',
    execution_timeout=timedelta(minutes=60),
    dag=dag
)
```
> **Warning**: while this alternative is very easy to deploy, it processes the data 
> inside Airflow, which personally I'm not a big fan 😅. I like to keep Airflow's 
> computing to orchestration only, and run all data processing tasks in a external and
> ephemeral infrastructure.

#### As a task on Airflow but running on external cluster:
To overcome the limitations of previous suggestion you can use a [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) 
(if you are already using a Kubernetes cluster) or a [ECSOperator](https://docs.aws.amazon.com/mwaa/latest/userguide/samples-ecs-operator.html)
(for a self-managed solution).

#### Other ideas:
Implement other entrypoints can enable other use cases! For instance, it's possible to 
implement a [FastAPI](https://github.com/tiangolo/fastapi) entrypoint and deploy this 
application as a REST API with endpoints to receive the records as payloads on PUT 
requests and upsert it in the database.

Another alternative is to implement a 
[Kafka consumer](https://docs.confluent.io/kafka-clients/python/current/overview.html#ak-consumer) 
entrypoint and deploy it as an event-driven app, receiving the records in a streaming 
topic.

## Software design references:
- [Book: Architecture Patterns with Python](https://www.amazon.com.br/dp/B085KB31X3/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)
