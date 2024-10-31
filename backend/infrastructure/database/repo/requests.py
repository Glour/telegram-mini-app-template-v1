from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.users import UserRepo
from infrastructure.database.setup import get_db


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.session)


@lru_cache
def get_database_repo(session: AsyncSession = Depends(get_db)) -> RequestsRepo:
    return RequestsRepo(session=session)
