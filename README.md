# Business Automation Labs CRM

A multi-niche, multi-country CRM foundation for Business Automation Labs.

## Foundation

- Frontend: Next.js Pages Router, React, TypeScript, and Tailwind CSS
- Backend: FastAPI with environment-based configuration
- Database: local SQLite by default; optional local PostgreSQL
- ORM and migrations: SQLAlchemy 2 and Alembic
- The default setup has no paid services, provider API keys, billing, or managed database requirement

## Phase 2 database scope

The database models organizations, users, teams and roles, niches, countries, regions and cities, search configurations, leads and contacts, source URLs, local email-validation results, score history, discovery-job records, assignments, CRM and status history, reminders, campaigns, email drafts, suppression, and do-not-contact records.

Lead source URLs, niche links, assignments, scores, status changes, and email-validation results are historical records. Selecting another niche in the UI must filter leads, not remove or overwrite lead records. New lead writes should use `backend/crm_services.py` so organization scope, geography, normalized matching, niche links, and source history are applied consistently.

The initial migration can create a new database or adopt the existing unversioned Phase 1 SQLite database. It adds columns and tables, backfills only from existing rows, and does not create organizations or production seed records. Existing rows with no organization mapping remain available with a nullable organization link; map them to a real organization before using tenant-scoped CRM operations.

See [backend/docs/phase-2-data-model.md](backend/docs/phase-2-data-model.md) for the Mermaid ERD and data-retention details.

This phase stores search configurations, discovery-job records, validation outcomes, and email drafts. It does not implement a scraper, an email verifier, or an email sender.

## Project map

    frontend/
      components/              App shell, error boundary, API health card
      pages/                   Next.js Pages Router
      src/lib/api.ts            Typed backend health client
      styles/globals.css        Tailwind entry point
    backend/
      main.py                   FastAPI app, CORS, health route
      settings.py               Local API configuration
      database.py               SQLite/PostgreSQL engine and UTC timestamp handling
      models.py                 Core SQLAlchemy models
      models_operations.py      CRM history, campaigns, and suppression models
      crm_services.py           Organization-scoped lead matching and CRM writes
      migrations/               Alembic environment and migration history
      run_migrations.py         Apply schema migrations
      test_db.py                Isolated SQLite tests
      docs/                     Phase 2 ERD and data model notes

## Requirements

- Python 3.11 or newer
- Node.js version supported by the locked Next.js release
- npm

Frontend dependencies are pinned in package.json and package-lock.json. Use npm ci.

## Run locally

Open two PowerShell terminals at the repository root.

### Terminal 1: backend and database

Install the backend dependencies:

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt

Apply database migrations:

    .\.venv\Scripts\python.exe backend/run_migrations.py

Start the API:

    .\.venv\Scripts\python.exe backend/main.py

The API listens on http://127.0.0.1:8000 by default. The SQLite database is stored at backend/crm.db regardless of the current working directory.

### Terminal 2: frontend

PowerShell on Windows may block the `npm.ps1` wrapper. Use `npm.cmd`:

    cd frontend
    npm.cmd ci
    npm.cmd run dev

Open http://localhost:3000.

If port 8000 is already occupied, check whether the CRM backend is already running before starting another copy:

    Invoke-RestMethod http://127.0.0.1:8000/health

## Configuration

Backend settings are read from backend/.env, then overridden by process environment variables:

- API_HOST: bind address; defaults to 127.0.0.1
- API_PORT: port; defaults to 8000 and must be between 1 and 65535
- FRONTEND_ORIGINS: comma-separated browser origins allowed by CORS
- DATABASE_URL: optional database URL; defaults to local backend/crm.db

The example SQLite URL is `sqlite:///./crm.db`; relative SQLite paths resolve from the backend directory. PostgreSQL can be used on a local server. Install its optional driver with:

    .\.venv\Scripts\python.exe -m pip install -r backend/requirements-postgres.txt

Then set DATABASE_URL in backend/.env, for example:

    DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/business_automation_labs

Do not put credentials in source control. No database or provider account is required for the default local setup.

Frontend settings are loaded from frontend/.env.local:

- NEXT_PUBLIC_API_BASE_URL: API origin, for example http://127.0.0.1:8000

NEXT_PUBLIC_ values are included in browser code. Never place secrets there. If you change the frontend host or port, update FRONTEND_ORIGINS and restart the backend.

## Verify

Run the isolated Phase 2 database tests:

    .\.venv\Scripts\python.exe backend/test_db.py

The tests use temporary SQLite databases and copy the current local database only for a read-only migration-preservation check. They do not insert test data into backend/crm.db.

Check the API response:

    Invoke-RestMethod http://127.0.0.1:8000/health

It should return `status: healthy` and `service: backend`.

Check the frontend types and production build from the frontend directory:

    npm.cmd run typecheck
    npm.cmd run build
