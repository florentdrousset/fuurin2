# API Architecture and Conventions (FastAPI)

This document explains how the API is organized in this repository, common FastAPI conventions, and why the API is versioned with `/api/v1`.

Scope reminder: The app tracks practice sessions and exposes statistics derived from those sessions. There are no lessons and works are always Japanese.


## Current layout (as implemented)

- `api/main.py`
  - FastAPI app factory, CORS, mounts the versioned router under `/api/v1`, system health endpoints.
- `api/routers/v1.py`
  - All versioned endpoints for now (entities and stats). Grouped by tags in Swagger.
- `api/schemas/`
  - Pydantic models for request/response DTOs (e.g., `summary.py`, `activity.py`).
- `api/db/`
  - `database.py`: engine and SessionLocal
  - `deps.py`: `get_db()` dependency for request‑scoped sessions
  - `models.py`: SQLAlchemy ORM models aligned with `model.md`
  - `seed.py`: simple data seed to demo the endpoints
- `api/alembic/`
  - Alembic migrations (managed from `start.sh` at container boot)
- `api/start.sh`
  - Runs migrations then starts Uvicorn

This structure is perfectly valid for a small/medium API. As the project grows, the most common evolution is to split the big router and schemas into per‑entity modules.


## Idiomatic FastAPI structure (recommended as the codebase grows)

A typical larger FastAPI project uses one module per “domain” (entity or feature):

- `api/main.py` — app setup (CORS, lifespan, mount routers)
- `api/routers/`
  - `v1/` (package)
    - `users.py` — `/api/v1/users` routes
    - `works.py` — `/api/v1/works` routes
    - `study_sessions.py` — `/api/v1/study-sessions` routes
    - `activity_events.py` — `/api/v1/activity-events` routes
    - `stats.py` — `/api/v1/stats/*` aggregate routes
    - `__init__.py` — exposes a combined `router` to mount in `main.py`
- `api/schemas/`
  - `users.py`, `works.py`, `study_sessions.py`, `activity_events.py`, `stats.py`
- `api/db/`
  - `models/` (optional split by entity) or keep a single `models.py` if you prefer
  - `database.py`, `deps.py`
- `api/services/` (optional) — reusable domain logic/queries that routers call
- `api/core/` (optional) — settings, auth, exceptions, utils

This is a style choice; both the current single‑file router and the split‑per‑entity layout are considered normal. The split aids discoverability when the endpoint set grows.


## Why `/api/v1` in the URL?

Versioning APIs by URL path is a widely used, simple strategy:

- Stability for clients: breaking changes go to a new version (`/api/v2`), existing clients can continue to use `v1`.
- Caching/CDN friendliness and easy routing at reverse proxies.
- Simple documentation: Swagger groups everything under one prefix.

Alternatives exist (header‑based versioning, media‑type versioning), but path versioning is the most straightforward for SPAs like this Svelte front.

Guidelines we follow:
- Additive changes (new optional fields/endpoints) keep the same `v1`.
- Breaking changes (remove/rename fields, change semantics, required params) → release `v2` alongside `v1` for a deprecation period.
- Keep `/health`, `/version`, and `/db/health` unversioned (they’re operational endpoints, not business API).


## URL design principles used here

- Entity‑centric RESTful collections with filters:
  - `GET /api/v1/users`, `GET /api/v1/users/{user_id}`
  - `GET /api/v1/study-sessions?user_id=&work_id=`
  - `GET /api/v1/activity-events?user_id=&limit=`
  - `GET /api/v1/works`
- Aggregations as a separate namespace:
  - `GET /api/v1/stats/daily?user_id=&start=&end=` (for heatmap, etc.)
  - `GET /api/v1/stats/weekly?user_id=&week=YYYY-Www`
- Transitional convenience routes under `Me (deprecated)` remain for now and can be removed once the front is fully wired to entity endpoints.


## When to split files further

- If `api/routers/v1.py` exceeds ~500–800 lines or becomes hard to navigate, split into per‑entity modules as outlined above.
- If `api/db/models.py` becomes unwieldy, split into `api/db/models/` package (one file per entity), and import their `Base` metadata for Alembic.
- If query logic becomes complex, move into `api/services/*` functions (e.g., `stats.py` computing streaks, weekly buckets, etc.).


## Coding conventions

- Tags in routes are used to group endpoints in Swagger by entity: Users, Works, Study Sessions, Activity Events, Reading Speeds, Stats, System, and Me (deprecated).
- Pydantic v2 is used for DTOs; response models should be declared for public endpoints to keep schemas stable.
- Database sessions: use `Depends(get_db)` from `db.deps` to get a request‑scoped `Session`.
- Migrations: any ORM change → create Alembic revision; in Docker we run `alembic upgrade head` on boot.


## FAQ

- Do we need “one file per class”? No. It’s a preference. For small projects a single `models.py` and a single `v1.py` router is fine. As we add features, splitting by entity is the common path in FastAPI projects.
- Is `/api/v1` mandatory? Not mandatory, but strongly recommended to avoid breaking clients later. Keeping it now costs little and gives flexibility later.
- Can we remove `/me/*`? Yes—once the front uses entity routes and stats endpoints, those can be removed. They’re tagged as deprecated in docs.


## Next steps (if we decide to modularize)

- Create `api/routers/v1/` package and move entity blocks from `v1.py` into dedicated files.
- Mirror the same structure in `api/schemas/` so each entity has its own DTOs.
- Keep `main.py` unchanged, still mounting a single combined `v1` router.
