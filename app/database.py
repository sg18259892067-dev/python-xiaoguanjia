from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.base import Base


engine = None
SessionLocal = None


def init_db(app):
    global engine
    global SessionLocal

    engine = create_engine(app.config["DATABASE_URL"])

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(engine)
