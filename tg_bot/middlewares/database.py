from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, repo: RequestsRepo) -> None:
        self.repo = repo

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user = await self.repo.users.get_or_create(
            user_id=event.from_user.id,
            first_name=event.from_user.first_name,
            full_name=event.from_user.full_name,
            language=event.from_user.language_code,
            username=event.from_user.username
        )

        data["user"] = user
        result = await handler(event, data)

        return result
