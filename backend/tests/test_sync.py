from httpx import AsyncClient

from src.calendar_providers.fixture_store import fixture_store

ALICE_GOOGLE = "c0000000-0000-0000-0000-00000000000a"
BOB_MICROSOFT = "c0000000-0000-0000-0000-00000000000b"


async def test_sync_returns_a_success_status(api: AsyncClient) -> None:
    response = await api.post("/api/meetings/sync")

    assert response.status_code == 204


def test_fixture_store_example() -> None:
    """Example of simulating a remote calendar change from a test; delete once you have real tests."""
    events = fixture_store.get().connections[ALICE_GOOGLE].events

    events[0].title = "Annual financial review (moved)"

    assert fixture_store.get().connections[ALICE_GOOGLE].events[0].title == "Annual financial review (moved)"
