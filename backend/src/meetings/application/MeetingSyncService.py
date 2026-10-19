from sqlalchemy.ext.asyncio import AsyncSession

from src.calendar_providers.stub_client import StubCalendarClient


class MeetingSyncService:
    """Pulls events from every connected calendar and reflects them as meetings in the platform."""

    def __init__(self, session: AsyncSession, calendar_client: StubCalendarClient) -> None:
        self._session = session
        self._calendar_client = calendar_client

    async def sync_all(self) -> None:
        raise NotImplementedError
