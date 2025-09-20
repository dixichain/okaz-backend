# Okaz Backend (POC)

**What this is:** A simple FastAPI backend that serves our POC endpoints for deals and parties, using PostgreSQL.

## Quick start (local)

1) Install Python 3.11+
2) Create and activate a virtual env:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

3) Install deps:
```bash
pip install -r requirements.txt
```

4) Set environment variables (create `.env`):
```
DATABASE_URL=postgresql://render_postgres_db_1vfe_user:n4rKi5tTM7S3dvhn6vrno5JAc3hkUoC9@dpg-d36oogeuk2gs73a6hpd0-a/render_postgres_db_1vfe
FRONTEND_ORIGIN=https://okaz-frontend.onrender.com
```

5) Run:
```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Deploy on Render

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Env vars:**
  - `DATABASE_URL` = postgresql://render_postgres_db_1vfe_user:n4rKi5tTM7S3dvhn6vrno5JAc3hkUoC9@dpg-d36oogeuk2gs73a6hpd0-a/render_postgres_db_1vfe
  - `FRONTEND_ORIGIN` = https://okaz-frontend.onrender.com

Make sure your database already has the schema loaded (run the SQL we generated earlier), then import CSVs.
