# Co-founder handoff: Phases 3 and 4

This guide starts from the committed Phase 1 and Phase 2 CRM foundation and explains how to build Phases 3 and 4 on top of it, then hand the work back for Phases 5 and 6.

## 1. Pull the Phase 1/2 baseline

The project owner should push the reviewed `main` branch to GitHub first. Then, in a fresh PowerShell window:

```powershell
git clone https://github.com/Business-Auto-Labs/business-auto-labs.git
Set-Location -LiteralPath .\business-auto-labs
git switch main
git pull --ff-only origin main
```

If the repository is already cloned:

```powershell
Set-Location -LiteralPath "C:\Users\<you>\path\business-auto-labs"
git switch main
git pull --ff-only origin main
```

Confirm the baseline includes the Phase 2 migration and ERD:

```powershell
git log -5 --oneline
Test-Path .\backend\migrations\versions\20261124_0001_phase2_core.py
Test-Path .\backend\docs\phase-2-data-model.md
```

Both `Test-Path` commands should return `True`.

## 2. Install and verify the baseline

Run these commands from the repository root. A fresh clone intentionally has no local database; the migration creates one:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe backend/run_migrations.py
.\.venv\Scripts\python.exe backend/test_db.py
```

In another terminal, install and run the frontend from its directory:

```powershell
Set-Location -LiteralPath .\frontend
npm.cmd ci
npm.cmd run typecheck
npm.cmd run dev
```

Use `npm.cmd` in Windows PowerShell 5.1 if script execution policy blocks `npm.ps1`. The API health check is `http://127.0.0.1:8000/health`; the frontend is `http://localhost:3000`. If port 8000 is occupied, check the health endpoint before starting another backend process.

Before coding, read:

- `README.md`
- `backend/docs/phase-2-data-model.md`
- `frontend/AGENTS.md` and the relevant installed Next.js documentation before changing frontend code

## 3. Work on a handoff branch

Keep `main` as the shared Phase 1/2 baseline. Create one feature branch for Phases 3 and 4:

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/phases-3-4
```

Implement Phase 3 and Phase 4 from the prompts supplied by the project owner. Keep each phase within its prompt and build on the existing project structure. Do not recreate Phase 1 or replace the Phase 2 database architecture.

### Foundation constraints to preserve

- Keep local SQLite as the zero-setup default. PostgreSQL is optional and local.
- Do not require paid APIs, data providers, scraping services, email verification, CRM integrations, billing, or provider keys.
- Phase 2 records search configurations, discovery jobs, validation results, and email drafts; it does not run discovery, verify emails through a service, or send email.
- Keep tenant-scoped writes organization-aware. Use `backend/crm_services.py` for lead/source/niche matching and CRM status changes.
- Add schema changes as new Alembic revisions. Do not edit migrations that have already been applied or rewrite history.
- Keep old leads when filters or selected niches change. Preserve source URLs and CRM history.
- Keep fixtures in temporary test databases. Never add generated fake prospects to a shared or production database.
- Do not commit `.env`, `.env.local`, `backend/crm.db`, SQLite backups, credentials, or generated build output.

## 4. Test and commit Phases 3/4

After each phase, run its required tests. Before handing back, run the project checks from the repository root:

```powershell
.\.venv\Scripts\python.exe backend/run_migrations.py
.\.venv\Scripts\python.exe backend/test_db.py
Push-Location .\frontend
npm.cmd run typecheck
Pop-Location
```

Review the files before committing. Verify local databases and secrets are ignored:

```powershell
git status --short
git check-ignore backend/crm.db
git diff --check
```

Commit the completed work on the feature branch:

```powershell
git add -A
git diff --cached --check
git diff --cached --stat
git commit -m "feat: complete Phases 3 and 4"
git push -u origin feature/phases-3-4
```

Send the project owner the branch name and commit hash. Do not push directly to `main`.

## 5. Bring Phases 3/4 back for Phases 5/6

The project owner can review and merge the feature branch through a GitHub pull request. After it is merged, update the local `main` branch:

```powershell
git switch main
git pull --ff-only origin main
```

If the owner is merging locally instead of using a pull request:

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git merge --no-ff origin/feature/phases-3-4
git push origin main
```

Start Phases 5 and 6 from the updated `main`, after confirming the Phase 3/4 migration and tests pass. Keep the Phase 3/4 branch and commits available for review.
