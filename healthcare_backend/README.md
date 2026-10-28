# Healthcare Backend

Django + Django REST Framework + PostgreSQL backend with JWT authentication (`djangorestframework-simplejwt`) for managing patients, doctors and patient-doctor assignments.

## Project structure

```
config/            settings, root urls, custom exception handler
apps/accounts/     custom email-based User, register + login (JWT)
apps/patients/     Patient model and CRUD
apps/doctors/      Doctor model and CRUD
apps/mappings/     Patient-doctor assignments
```

## Setup (Windows PowerShell)

1. **Create the database** (PostgreSQL must be installed and running):
   ```
   psql -U postgres -c "CREATE DATABASE healthcare_db;"
   ```
2. **Create and activate the virtualenv, install dependencies**:
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. **Configure environment variables**: copy `.env.example` to `.env` and fill in the values.
   ```
   copy .env.example .env
   ```
   Set `DB_PORT` to the port your PostgreSQL server listens on (the default is 5432; check `port` in `postgresql.conf`).
   Generate a secret key with:
   ```
   python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
   ```
4. **Migrate and run**:
   ```
   python manage.py migrate
   python manage.py createsuperuser   # optional, for /admin/
   python manage.py runserver
   ```

The API is served at `http://127.0.0.1:8000/api/`, and a simple web UI for registering, logging in and managing patients, doctors and assignments is at `http://127.0.0.1:8000/`. If port 8000 is taken, run `python manage.py runserver 8001` and use that port instead.

## Authentication

Register, then log in to get tokens. Send the access token on every other request:

```
Authorization: Bearer <access token>
```

| Method | Endpoint | Body | Notes |
|---|---|---|---|
| POST | `/api/auth/register/` | `name`, `email`, `password` | Public |
| POST | `/api/auth/login/` | `email`, `password` | Returns `access` and `refresh` |
| POST | `/api/auth/token/refresh/` | `refresh` | Returns a new `access` token |

## Endpoints (all require a JWT)

### Patients
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Add a patient |
| GET | `/api/patients/` | List patients you created |
| GET | `/api/patients/<id>/` | Patient details |
| PUT | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

Fields: `name`, `age`, `gender` (`M`/`F`/`O`), `phone`, `address`, `medical_history`.
Patients are private to the user who created them; other users get `404`.

### Doctors
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Doctor details |
| PUT | `/api/doctors/<id>/` | Update a doctor (creator only, otherwise `403`) |
| DELETE | `/api/doctors/<id>/` | Delete a doctor (creator only, otherwise `403`) |

Fields: `name`, `specialization`, `email` (unique), `phone`, `experience_years`.

### Mappings
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient: `{"patient": 1, "doctor": 1}` |
| GET | `/api/mappings/` | All mappings for your patients |
| GET | `/api/mappings/<patient_id>/` | Doctors assigned to that patient |
| DELETE | `/api/mappings/<id>/` | Remove a doctor from a patient (`<id>` is the mapping id) |

You can only assign doctors to patients you created, and a doctor can be assigned to a given patient only once.

## Error responses

Validation problems return `400` with field-level messages, e.g. `{"email": ["A user with this email already exists."]}`. Missing or invalid tokens return `401`, forbidden changes `403`, and unknown or inaccessible records `404`.

## Testing with Postman

1. `POST /api/auth/register/`, then `POST /api/auth/login/` and copy the `access` token.
2. In the collection's **Authorization** tab choose *Bearer Token* and paste it.
3. Create a patient and a doctor, then `POST /api/mappings/` with their ids.
