"""Repository dependancies for FastApi app.

TODO:
    1. do funcs need to be async?
"""
from typing import Callable, TypeVar, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import get_current_username
from app.db.base import SQLAlchemyRepository

from app.routes.session import get_async_session


RepositoryType = TypeVar("RepositoryType", bound=SQLAlchemyRepository)


# Repo dependency
def get_repository(
    repo_type: Type[RepositoryType],
    ) -> Callable[[AsyncSession], Type[RepositoryType]]:
    """Returns specified repository seeded with an async database session."""
    def get_repo(
        db: AsyncSession = Depends(get_async_session),
        username: str = Depends(get_current_username),
    ) -> Type[RepositoryType]:
        return repo_type(db=db, username=username)

    return get_repo
