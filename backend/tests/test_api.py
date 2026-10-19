from httpx import AsyncClient


async def test_lists_seeded_calendar_connections(api: AsyncClient) -> None:
    response = await api.get("/api/calendar-connections")

    assert response.status_code == 200
    assert {(c["advisor"]["name"], c["provider"]) for c in response.json()} == {
        ("Alice Carter", "GOOGLE"),
        ("Bob Singh", "MICROSOFT"),
    }


async def test_meetings_are_empty_before_any_sync(api: AsyncClient) -> None:
    response = await api.get("/api/meetings")

    assert response.status_code == 200
    assert response.json() == []


async def test_calendar_fixture_can_be_replaced(api: AsyncClient) -> None:
    fixture = (await api.get("/dev/calendar-fixture")).json()
    fixture["connections"]["c0000000-0000-0000-0000-00000000000b"]["fail"] = True

    await api.put("/dev/calendar-fixture", json=fixture)

    updated = (await api.get("/dev/calendar-fixture")).json()
    assert updated["connections"]["c0000000-0000-0000-0000-00000000000b"]["fail"] is True
