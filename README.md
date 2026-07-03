# FastAPI Authentication API

A REST API built with **FastAPI**, **SQLModel**, **PostgreSQL**, **Alembic**, and **Docker**. This project implements user authentication using JWT tokens along with CRUD operations for users and posts.

## Features

* User registration
* JWT-based authentication
* Password hashing
* Protected routes
* User CRUD operations
* Post CRUD operations
* User ↔ Post relationship
* PostgreSQL database
* Alembic database migrations
* Docker & Docker Compose support
* Input validation using Pydantic
* SQLModel ORM

---

## Tech Stack

* Python 3.12
* FastAPI
* SQLModel
* SQLAlchemy
* PostgreSQL
* Alembic
* Docker
* Passlib / Argon2
* PyJWT

---

## Project Structure

```
.
├── app/
│   ├── auth/
│   ├── users/
│   ├── posts/
│   ├── database/
│   ├── model_registry.py
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── alembic.ini
```

---

## Authentication

Authentication is implemented using OAuth2 Password Flow with JWT access tokens.

### Public Endpoints

| Method | Endpoint  | Description           |
| ------ | --------- | --------------------- |
| POST   | `/signup` | Register a new user   |
| POST   | `/token`  | Login and receive JWT |

All other endpoints require a Bearer token.

---

## User Endpoints

| Method | Endpoint              | Description                 |
| ------ | --------------------- | --------------------------- |
| GET    | `/user`               | Get all users               |
| GET    | `/users/{user_id}`    | Get user by ID              |
| PATCH  | `/users/me/update`    | Update current user         |
| DELETE | `/users/me/delete`    | Delete current user         |
| GET    | `/getposts/{user_id}` | Get posts created by a user |

---

## Post Endpoints

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| POST   | `/posts/`             | Create a post        |
| GET    | `/posts/`             | List posts           |
| GET    | `/posts/{post_id}`    | Get a post           |
| PATCH  | `/posts/{post_id}`    | Update your own post |
| DELETE | `/posts/{post_id}`    | Delete your own post |
| GET    | `/getowner/{post_id}` | Get owner of a post  |

---

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd app-auth
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it.

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file for local development by copying:

```bash
cp .env.example .env
```

For Docker, create a `.env.docker` file with the same variables as `.env.example`, but set Docker-specific values where necessary.

For example:

| Variable | Local | Docker |
|----------|-------|--------|
| DATABASE_HOST | localhost | db |
| DATABASE_PORT | 5432 | 5432 |

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
fastapi dev app/main.py
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Running with Docker

Build and start the containers.

```bash
docker compose up --build
```

Run migrations after the containers start.

```bash
docker compose exec api alembic upgrade head
```

Application:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

## Database

The application uses PostgreSQL with Alembic for schema versioning.

Current entities include:

* User
* Post

Relationship:

```
User
 └── has many Posts
```

---

## Security

* Passwords are securely hashed before storage.
* JWT Bearer authentication protects private endpoints.
* Users can only modify or delete their own resources.
* Input validation is handled using Pydantic models.

## API Testing

A comprehensive Postman collection is included to verify the API's functionality.

### Coverage

The collection contains automated tests for:

- User authentication (signup and login)
- User CRUD operations
- Post CRUD operations
- Authorization and authentication
- Input validation
- Success and failure scenarios
- Pagination endpoints

Tests validate:

- HTTP status codes
- Response schema
- Returned values
- Data types
- Validation error responses
- Authorization behavior

### Running the collection

1. Import the Postman collection.
2. Import the sample Postman environment.
3. Set the required environment variables.
4. Start the API.
5. Run the collection using the Collection Runner.

### Environment variables

The following variables must be configured before running the collection:

| Variable | Description |
|----------|-------------|
| `base_url` | Base URL of the API |
| `target_user_id` | Existing user ID used for read operations |
| `target_full_name` | Expected full name of the target user |
| `target_username` | Expected username of the target user |
| `target_email` | Expected email of the target user |
| `target_post_id` | Existing post used for read operations |
| `foreign_post_id` | Post ID used for authorization tests |
| `offset` | Pagination offset |
| `limit` | Pagination limit |
| `fake_access_token` | Invalid JWT used for authentication tests |
| `short_password` | Password shorter than the minimum length |
| `wrong_email_@` | Email missing the `@` symbol |
| `wrong_email_username` | Email missing the username before `@` |

The remaining variables (such as `access_token`, `user_id`, `owned_post_id`, `user_name`, `password`, and `email`) are generated automatically while the collection runs.

## Future Improvements

* Refresh tokens
* Role-based authorization
* Email verification
* Password reset
* Unit and integration tests
* CI/CD pipeline
* API rate limiting
* Logging and monitoring

---

## Learning Goals

This project was built to practice:

* FastAPI
* SQLModel
* Database relationships
* Authentication & authorization
* Alembic migrations
* Docker containerization
* REST API design
* Input validation
* Project organization
