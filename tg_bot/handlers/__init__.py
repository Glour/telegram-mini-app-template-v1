"""Import all routers and add them to routers_list."""
from aiogram import Router, F

from filters.admin import AdminFilter
from handlers.errors import bot_api_errors
from handlers.user import start
from settings import settings

admin_router = Router()

if not settings.is_development:
    admin_router.message.filter(AdminFilter())

admin_router.include_routers(*[])

user_router = Router()
user_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))
user_router.include_routers(*[
    start.router,
])

error_router = Router()
error_router.include_router(bot_api_errors.router)

channels_router = Router()
channels_router.message.filter(F.chat.func(lambda chat: chat.type in ("group", "supergroup", "channel")))
channels_router.include_routers(*[])

routers_list = [
    user_router,
    admin_router,
    channels_router,
    error_router,
]

__all__ = [
    "routers_list",
]
