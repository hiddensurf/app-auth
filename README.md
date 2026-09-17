# FastAPI JWT Authentication API

A container-ready FastAPI backend for user registration, OAuth2/JWT login, protected user access, and user-owned post management.

## What the code demonstrates

- User signup with validation and password hashing
- OAuth2 password flow with signed JWT access tokens
- Protected routes backed by the current authenticated user
- Post creation plus ownership checks for update and delete operations
- PostgreSQL persistence, SQLAlchemy models, and Alembic migrations
- Dockerfile and Docker Compose setup
- pytest fixtures for API tests against a separate PostgreSQL test database
- An included Postman collection for exercising the API

## Run with Docker Compose

```bash
git clone https://github.com/hiddensurf/app-auth.git
cd app-auth
cp .env.example .env
docker compose up --build
```

Review the example environment values before starting. The API exposes interactive OpenAPI docs at `/docs` while running.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

Set the environment variables shown in the repository's example files, make PostgreSQL available, then run:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

## Test setup

The repository includes pytest fixtures, a FastAPI `TestClient`, generated user data, and dependency overrides for a separate PostgreSQL test database. Add or run test modules against that setup with `pytest`.

## API evidence

The repository also includes a Postman collection that can be imported to inspect and call the implemented endpoints without building a separate client.
