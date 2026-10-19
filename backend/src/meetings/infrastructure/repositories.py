from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.meetings.infrastructure.entities import CalendarConnectionEntity, ClientEntity, MeetingEntity


class MeetingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> Sequence[MeetingEntity]:
        result = await self._session.scalars(select(MeetingEntity).order_by(MeetingEntity.starts_at))
        return result.all()


class CalendarConnectionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> Sequence[CalendarConnectionEntity]:
        result = await self._session.scalars(
            select(CalendarConnectionEntity).order_by(CalendarConnectionEntity.connected_at)
        )
        return result.all()


class ClientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> Sequence[ClientEntity]:
        result = await self._session.scalars(select(ClientEntity).order_by(ClientEntity.name))
        return result.all()
