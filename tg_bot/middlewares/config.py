from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.database.repo.requests import RequestsRepo
from settings.app_settings import AppSettings


class ConfigMiddleware(BaseMiddleware):
    def __init__(
            self,
            settings: AppSettings,
            scheduler: AsyncIOScheduler,
            repo: RequestsRepo
    ) -> None:
        self.settings = settings
        self.scheduler = scheduler
        self.repo = repo

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        data["settings"] = self.settings
        data["scheduler"] = self.scheduler
        data["repo"] = self.repo

        return await handler(event, data)
