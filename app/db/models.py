
from sqlalchemy import Table
from app.db.base import SQLAlchemyRepository
from db_session import metadata
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=metadata)


class Users(SQLAlchemyRepository):
    model = Table('users', metadata, autoload=True)

