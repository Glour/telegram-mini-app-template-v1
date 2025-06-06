from typing import Any, Optional, Type, TypeVar

from sqlalchemy import update, delete, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar('T', bound=DeclarativeMeta)


class BaseRepo:
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, obj_id: Any) -> Optional[T]:
        stmt = (
            select(self.model)
            .filter_by(id=obj_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Optional[T]:
        insert_stmt = (
            insert(self.model)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def create_on_conflict_do_nothing(self, **kwargs) -> Optional[T]:
        if not kwargs:
            kwargs = {}

        insert_stmt = (
            insert(self.model)
            .values(**kwargs)
            .on_conflict_do_nothing(
                index_elements=[self.model.id],
            )
            .returning(self.model)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def update(self, obj_id: Any | list[Any], **kwargs) -> T | list[T] | None:
        if not obj_id:
            return

        if isinstance(obj_id, list):
            stmt = (
                update(self.model)
                .values(**kwargs)
                .where(self.model.id.in_(obj_id))
                .execution_options(synchronize_session="fetch")
                .returning(self.model)
            )
        else:
            stmt = (
                update(self.model)
                .values(**kwargs)
                .filter_by(id=obj_id)
                .returning(self.model)
            )
        result = await self.session.execute(stmt)
        await self.session.commit()

        if isinstance(obj_id, list):
            return list(result.scalars().all())

        return result.scalar_one_or_none()

    async def delete(self, obj_id: Any | list[Any]) -> list[T] | None:
        if isinstance(obj_id, list):
            stmt = (
                delete(self.model)
                .filter(self.model.id.in_(obj_id))
                .returning(self.model)
            )
        else:
            stmt = (
                delete(self.model)
                .filter_by(id=obj_id)
                .returning(self.model)
            )

        result = await self.session.execute(stmt)
        await self.session.commit()

        if isinstance(obj_id, list):
            return list(result.scalars().all())
        else:
            return result.scalar_one_or_none()

    async def get_all(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> list[T]:
        stmt = (
            select(self.model)
            .order_by(self.model.id)
        )

        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_all(self) -> int:
        stmt = (
            select(func.count())
            .select_from(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar()
