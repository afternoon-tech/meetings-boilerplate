from fastapi import APIRouter, status

from src.calendar_providers.fixture_store import CalendarFixture, fixture_store

router = APIRouter(prefix="/dev", tags=["dev"])


@router.get("/calendar-fixture")
async def get_calendar_fixture() -> CalendarFixture:
    """What each stubbed calendar returns on its next fetch."""
    return fixture_store.get()


@router.put("/calendar-fixture", status_code=status.HTTP_204_NO_CONTENT)
async def replace_calendar_fixture(fixture: CalendarFixture) -> None:
    """Simulates changes made in the remote calendars (an event moved, cancelled, a provider outage...)."""
    fixture_store.replace(fixture)


@router.post("/calendar-fixture/reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset_calendar_fixture() -> None:
    fixture_store.reset()
