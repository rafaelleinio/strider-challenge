import pytest
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture
def in_memory_db():
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def session(in_memory_db):
    SQLModel.metadata.create_all(in_memory_db)
    yield Session(in_memory_db)
