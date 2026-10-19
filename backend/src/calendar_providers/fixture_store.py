import json
from pathlib import Path

from pydantic import BaseModel

from src.calendar_providers.domain import ExternalCalendarEvent

DEFAULT_FIXTURE_PATH = Path(__file__).parent / "fixtures" / "default.json"


class ConnectionFixture(BaseModel):
    fail: bool = False
    events: list[ExternalCalendarEvent] = []


class CalendarFixture(BaseModel):
    """What each connected calendar will return on its next fetch, keyed by calendar connection id."""

    connections: dict[str, ConnectionFixture]


class FixtureStore:
    """In-memory stand-in for the providers' remote state. Swappable at runtime through the dev router."""

    def __init__(self) -> None:
        self._fixture = self.load_default()

    @staticmethod
    def load_default() -> CalendarFixture:
        return CalendarFixture.model_validate(json.loads(DEFAULT_FIXTURE_PATH.read_text()))

    def get(self) -> CalendarFixture:
        return self._fixture

    def replace(self, fixture: CalendarFixture) -> None:
        self._fixture = fixture

    def reset(self) -> None:
        self._fixture = self.load_default()


fixture_store = FixtureStore()
