# Meetings

A cut-down slice of our financial advisor platform: advisors connect their Google or Microsoft calendars, and their
client meetings show up in the platform.

The task itself is shared at the start of the interview. Before then, please get the project running and have a look
around. You're welcome (and encouraged) to use whatever AI coding tools you'd normally use.

## Stack

- **API** (`backend/`): Python 3.13, FastAPI, SQLAlchemy 2 (async), PostgreSQL, pytest. Managed with [uv](https://docs.astral.sh/uv/).
- **Web** (`frontend/`): React 19, TypeScript, Vite, Mantine 9, TanStack Query 5, Vitest. Managed with [pnpm](https://pnpm.io/).
- **Database**: PostgreSQL 16 in Docker.

## Getting started

Prerequisites: Docker, uv, Node 22 and pnpm.

```bash
make setup     # starts Postgres, installs dependencies, creates and seeds the schema
make api       # http://localhost:8000 (API docs at /docs)
make web       # http://localhost:5173
make test      # back-end and front-end tests
```

One back-end test (`test_sync_returns_a_success_status`) fails on purpose: sync is not implemented yet.

## What's here

| Area | Where | Notes |
| --- | --- | --- |
| Database entities | `backend/src/meetings/infrastructure/entities.py` | Advisors, clients, calendar connections, meetings. Change freely. |
| Schema | `backend/src/seed.py` | No migrations: edit the entities, then `make db-reset` (drops everything and reseeds). |
| API | `backend/src/meetings/adaptors/routers.py` | `GET /api/meetings`, `POST /api/meetings/sync`, `GET /api/calendar-connections`, `GET /api/clients` |
| Sync | `backend/src/meetings/application/MeetingSyncService.py` | Not implemented. |
| Calendar providers | `backend/src/calendar_providers/` | Stubbed. No OAuth or SDKs: `StubCalendarClient.fetch_events(connection_id)` returns already-normalised events. |
| Calendar data | `backend/src/calendar_providers/fixtures/default.json` | What each connected calendar contains. |
| Meetings page | `frontend/src/pages/MeetingsPage.tsx` | Lists meetings, triggers a sync. |

### Simulating calendar changes

The stubbed calendars read from an in-memory fixture you can swap at runtime, so you can simulate someone moving or
cancelling an event in Google or Outlook:

- In the UI: **Calendar fixture** (top right) lets you edit and save it.
- Over HTTP: `GET` / `PUT /dev/calendar-fixture`, `POST /dev/calendar-fixture/reset`.
- In tests: `fixture_store` from `src.calendar_providers.fixture_store` (see `backend/tests/test_sync.py`).

A connection with `"fail": true` makes `fetch_events` raise `CalendarProviderError`, as a provider outage would.

### Seed data

| Advisor | Calendar | Connection id |
| --- | --- | --- |
| Alice Carter | Google | `c0000000-0000-0000-0000-00000000000a` |
| Bob Singh | Microsoft | `c0000000-0000-0000-0000-00000000000b` |

Clients: John Smith, Jane Smith, Sarah Jones, David Brown, Emma Wilson (matched by email address in calendar invites).

## Conventions

See `CLAUDE.md`. In short: British English and sentence case in anything user-facing; tests for behaviour you add.
