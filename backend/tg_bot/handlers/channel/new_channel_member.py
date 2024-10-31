from aiogram import Router, F
from aiogram.types import ChatMemberUpdated

from infrastructure.database.models.users import User
from infrastructure.database.repo.requests import RequestsRepo
from settings import settings

router = Router()


@router.chat_member(F.new_chat_member.status == "member")
async def new_channel_member(event: ChatMemberUpdated, user: User, repo: RequestsRepo):
    if event.new_chat_member.status == "member" and not event.from_user.is_bot:
        pass
