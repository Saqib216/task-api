# Task API

A FastAPI-based task management system with role-based access control (Admin / Employee), JWT authentication, and SQLModel ORM supporting both SQLite and PostgreSQL.

## Deployment

### Prerequisites & Configuration

When deploying to production (e.g. Heroku, Render, Railway), ensure the following environment variables are set in your platform's configuration dashboard:

| Variable Name | Description |
| :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string (automatically provided by cloud PostgreSQL add-ons like Heroku Postgres / Neon). |
| `SECRET_KEY` | Secret key used to sign and verify JWT authentication tokens. |
| `ALGORITHM` | JWT signing algorithm (defaults to `HS256`). |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifespan in minutes (defaults to `30`). |
| `ADMIN_EMAIL` | Email address for seeding the initial Administrator account. |
| `ADMIN_PASSWORD` | Password for seeding the initial Administrator account. |
| `ADMIN_NAME` | (Optional) Display name for the initial Administrator account. |

### Running the App

The project includes a `Procfile` for container / platform execution:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Initial Admin Seeding

After deploying and setting environment variables, run the seeding script once via your platform's CLI / one-off dyno:

```bash
python seed.py
```

