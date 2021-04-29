from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://andrii:password@localhost/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(bind=engine,
                             autoflush=False,
                             autocommit=False,
                             )
Base = declarative_base()
