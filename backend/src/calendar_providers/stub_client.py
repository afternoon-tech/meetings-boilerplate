import asyncio
import random

from src.calendar_providers.domain import CalendarProviderError, ExternalCalendarEvent
from src.calendar_providers.fixture_store import FixtureStore, fixture_store


class StubCalendarClient:
    """Stands in for the Google Calendar and Microsoft Graph clients.

    Returns every event in the connection's calendar within the sync window. A real client would page
    through results and could return incremental changes; this stub always returns the full list.
    """

    def __init__(self, store: FixtureStore = fixture_store, max_latency_seconds: float = 0.3) -> None:
        self._store = store
        self._max_latency_seconds = max_latency_seconds

    async def fetch_events(self, calendar_connection_id: str) -> list[ExternalCalendarEvent]:
        await asyncio.sleep(random.uniform(0, self._max_latency_seconds))
        connection = self._store.get().connections.get(calendar_connection_id)
        if connection is None:
            return []
        if connection.fail:
            raise CalendarProviderError(f"Provider unavailable for connection {calendar_connection_id}")
        return [event.model_copy(deep=True) for event in connection.events]


def get_calendar_client() -> StubCalendarClient:
    return StubCalendarClient()
