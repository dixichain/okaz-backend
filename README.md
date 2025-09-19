# Okaz Backend (POC)

**What this is:** A simple FastAPI backend that serves our POC endpoints for deals and parties, using PostgreSQL.

## Quick start (local)

1) Install Python 3.11+
2) Create and activate a virtual env:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

3) Install deps:
```bash
pip install -r requirements.txt
```

4) Set environment variables (create `.env`):
```
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
FRONTEND_ORIGIN=https://your-frontend.onrender.com
```

5) Run:
```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Deploy on Render

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- **Env vars:**
  - `DATABASE_URL` = your Render Postgres connection string
  - `FRONTEND_ORIGIN` = your frontend URL (or `*` during testing)

Make sure your database already has the schema loaded (run the SQL we generated earlier), then import CSVs.
