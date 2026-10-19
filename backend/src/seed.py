"""Drops and recreates every table, then seeds advisors, clients and calendar connections.

There is no migration tool in this project: change the SQLAlchemy entities, then run `make db-reset`.
"""

import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.calendar_providers.domain import CalendarProvider
from src.database import Base
from src.meetings.infrastructure import entities  # noqa: F401  (registers every entity on Base.metadata)
from src.meetings.infrastructure.entities import AdvisorEntity, CalendarConnectionEntity, ClientEntity
from src.settings import settings

ALICE_ID = uuid.UUID("a0000000-0000-0000-0000-000000000001")
BOB_ID = uuid.UUID("a0000000-0000-0000-0000-000000000002")
ALICE_GOOGLE_CONNECTION_ID = uuid.UUID("c0000000-0000-0000-0000-00000000000a")
BOB_MICROSOFT_CONNECTION_ID = uuid.UUID("c0000000-0000-0000-0000-00000000000b")


async def recreate_schema(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def seed(session: AsyncSession) -> None:
    session.add_all(
        [
            AdvisorEntity(id=ALICE_ID, name="Alice Carter", email="alice@harbourwealth.co.uk"),
            AdvisorEntity(id=BOB_ID, name="Bob Singh", email="bob@harbourwealth.co.uk"),
        ]
    )
    await session.flush()
    session.add_all(
        [
            CalendarConnectionEntity(
                id=ALICE_GOOGLE_CONNECTION_ID,
                advisor_id=ALICE_ID,
                provider=CalendarProvider.GOOGLE,
                account_email="alice@harbourwealth.co.uk",
            ),
            CalendarConnectionEntity(
                id=BOB_MICROSOFT_CONNECTION_ID,
                advisor_id=BOB_ID,
                provider=CalendarProvider.MICROSOFT,
                account_email="bob@harbourwealth.co.uk",
            ),
            ClientEntity(name="John Smith", email="john.smith@example.com"),
            ClientEntity(name="Jane Smith", email="jane.smith@example.com"),
            ClientEntity(name="Sarah Jones", email="sarah.jones@example.com"),
            ClientEntity(name="David Brown", email="david.brown@example.com"),
            ClientEntity(name="Emma Wilson", email="emma.wilson@example.com"),
        ]
    )
    await session.commit()


async def main() -> None:
    engine = create_async_engine(settings.database_url)
    await recreate_schema(engine)
    async with AsyncSession(engine) as session:
        await seed(session)
    await engine.dispose()
    print("Database reset and seeded.")


if __name__ == "__main__":
    asyncio.run(main())
