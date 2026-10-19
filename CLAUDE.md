# CLAUDE.md

See `README.md` for the stack, layout and commands.

- UK product: British English spelling in all user-facing text, comments and docs (organised, behaviour, cancelled).
- Sentence case for all UI text ("Sync meetings", not "Sync Meetings").
- Back end layering: `domain/` (models), `application/` (use cases), `infrastructure/` (database), `adaptors/` (HTTP).
- API schemas extend `CamelModel`: snake_case in Python, camelCase on the wire.
- Comments explain why, not what.
- Back-end tests run against a real Postgres database (`meetings_test`); each test starts from a freshly seeded schema.
- Checks: `make test`, `make check`.
