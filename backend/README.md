# AIVOA Customer Complaint Copilot

A portfolio-sized complaint-management application with a FastAPI/PostgreSQL backend and a React/Vite frontend. Authenticated users can create structured complaints through an AI-assisted intake flow, upload text PDFs, edit records conversationally, review risk assessments, and inspect an audit history.

## Architecture

```mermaid
flowchart LR
	Browser[React + Vite frontend] -->|Bearer JWT / JSON / multipart PDF| API[FastAPI API]
	API --> Auth[Auth service]
	API --> Complaints[Complaint and audit services]
	API --> Documents[PDF extraction service]
	API --> AI[LLM service]
	Auth --> DB[(PostgreSQL)]
	Complaints --> DB
	Documents --> DB
	Documents --> Files[(Upload directory)]
	AI --> Gemini[Google Gemini API]
```

The API owns authentication, authorization, validation, database writes, file paths, and audit events. The model only returns validated structured data; it cannot call tools or mutate the database.

## Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- PostgreSQL 14+ with a database created for this project
- A Google AI Studio API key and access to the configured Gemini model

## Backend setup

From `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and provide real values for `DATABASE_URL`, `SECRET_KEY`, `GOOGLE_API_KEY`, and `GOOGLE_MODEL`. Generate a long random `SECRET_KEY`; do not commit `.env` or expose `GOOGLE_API_KEY`.

Apply the schema and start the API:

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Health check: `GET /`. Interactive API documentation is available at `/docs`; the OpenAPI document is available at `/openapi.json`.

## Frontend setup

From `frontend`:

```powershell
npm install
Copy-Item .env.example .env
```

Set `VITE_API_BASE_URL=http://127.0.0.1:8000/api` in `frontend/.env`, then run:

```powershell
npm run dev
```

Open `http://127.0.0.1:5173`. For a production bundle, run `npm run build` and `npm run preview`.

## Environment variables

### Backend

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | PostgreSQL SQLAlchemy URL, for example `postgresql+psycopg://user:password@host:5432/database` |
| `SECRET_KEY` | Yes | At least 32 characters; signs JWTs |
| `ALGORITHM` | No | JWT algorithm; currently `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT lifetime; defaults to `30` |
| `GOOGLE_API_KEY` | Yes | Google AI Studio API key |
| `GOOGLE_MODEL` | No | Gemini model; defaults to `gemini-3-flash-preview` |
| `UPLOAD_DIR` | No | Server-side PDF storage directory; defaults to `uploads` |
| `MAX_FILE_SIZE_MB` | No | Maximum upload size; defaults to `10` |
| `FRONTEND_URL` | No | Allowed browser origin; defaults to `http://127.0.0.1:5173/` |

### Frontend

| Variable | Required | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Yes | FastAPI base URL including `/api`, with no trailing slash required |

Only public frontend configuration belongs in `VITE_*` variables. Never put tokens or passwords in frontend environment files.

## API overview

All routes except registration, login, and health require `Authorization: Bearer <access_token>`.

| Method | Path | Request | Response |
| --- | --- | --- | --- |
| `POST` | `/api/auth/register` | JSON: `email`, `full_name`, `password` | `UserResponse` |
| `POST` | `/api/auth/login` | Form: `username`, `password` | `TokenResponse` |
| `GET` | `/api/auth/me` | Bearer token | `UserResponse` |
| `GET` | `/api/complaints` | Bearer token | `ComplaintResponse[]` |
| `POST` | `/api/complaints` | `ComplaintCreate` JSON | `ComplaintResponse` |
| `GET` | `/api/complaints/{complaint_id}` | Bearer token | `ComplaintResponse` |
| `PUT` | `/api/complaints/{complaint_id}` | Partial `ComplaintUpdate` JSON | `ComplaintResponse` |
| `DELETE` | `/api/complaints/{complaint_id}` | Bearer token | `204 No Content` |
| `POST` | `/api/chat/log` | JSON: `message` | complaint plus risk assessment |
| `POST` | `/api/chat/edit` | JSON: `complaint_id`, `message` | updated complaint plus risk assessment |
| `POST` | `/api/document/extract` | Multipart: `complaint_id`, `file` | document, complaint, risk assessment |
| `GET` | `/api/audit/{complaint_id}` | Bearer token | `AuditResponse[]` |

Use `/docs` as the authoritative interactive reference for field constraints and response schemas. Dates use ISO `YYYY-MM-DD`; IDs use UUID strings.

## Database migrations

```powershell
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "describe the schema change"
```

Complaints, risk assessments, and documents are owned by a user and use cascading foreign keys. Audit rows deliberately do not have a complaint foreign key after migration `0002`, so deletion preserves historical events; audit `user_id` uses `SET NULL` when an account is removed.

## Security and AI boundaries

- Passwords are bcrypt-hashed and JWTs expire according to configuration.
- Every complaint, document, chat edit, and audit lookup is scoped to the authenticated user.
- PDF uploads require a `.pdf` filename, `application/pdf` MIME type, a bounded size, and successful text extraction. Files are stored under generated UUID filenames.
- Customer messages and extracted PDF text are serialized as untrusted data in a separate user message. Embedded instructions cannot change application behavior.
- AI input is length-limited. Responses require strict JSON schema validation, forbid unknown top-level fields, and use `null` for unavailable complaint fields.
- New AI complaints must include a product name and problem description before database creation. Existing complaints merge only non-null extracted values, preserving known data.
- Risk levels are constrained to `Critical`, `Major`, or `Minor`; AI output is validated before persistence.
- Audit events capture create, update, delete, AI extraction/edit, document upload, status changes, and risk changes.

This project does not implement production-grade abuse controls such as login rate limiting, refresh-token revocation, or malware scanning. Add those controls before exposing the service to the public internet.