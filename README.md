# FastAPI SQLite + Alembic + JWT + RBAC Example

## Setup

1. Create virtualenv and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run Alembic migrations:

```bash
alembic upgrade head
```

3. Start the server:

```bash
uvicorn app.main:app --reload
```

4. Run tests:

```bash
pytest -q
```

# Notes

- Update `app/security.py` SECRET_KEY for production.
- Alembic is configured to use the sqlite url in `alembic.ini`. You can change `DATABASE_URL` env var instead.

# End of project files
