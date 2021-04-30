from typing import Iterator
from functools import lru_cache

from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "postgresql://andrii:password@localhost/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(bind=engine,
                             autoflush=False,
                             autocommit=False,
                             )
Base = declarative_base()
metadata = Base.metadata


def get_db() -> Iterator[Session]:
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    return FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)
