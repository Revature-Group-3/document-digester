from collections.abc import Iterator
from functools import lru_cache

from document_digester.settings import settings
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseNotConfiguredError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    # Created lazily so the API can start (and vector/RAG endpoints work)
    # even when PostgreSQL is not configured.
    if not settings.DATABASE_URL:
        raise DatabaseNotConfiguredError(
            "DATABASE_URL is not set; SQL search is unavailable."
        )
    return create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


@lru_cache(maxsize=1)
def _session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)


def SessionLocal() -> Session:
    return _session_factory()()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
