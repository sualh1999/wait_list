# PLAN — Waitlist App

Status: Complete

## Overview
Build Waitlist App: FastAPI backend + Next.js frontend + Supabase + Resend + Docker (backend). Deploy backend to Render and frontend to Vercel.

## Checklist

### 0. Repo initialize
- [x] Create repo skeleton, .gitignore, .env.example, README.md, PLAN.md

### 1. Backend basic
- [x] Create FastAPI app skeleton (app/main.py)
- [x] Setup async SQLAlchemy + models + migrations notes
- [x] Implement /waitlist POST endpoint
- [x] Implement duplicate email check (db unique constraint)
- [x] Implement Resend email util (email on success)
- [x] Implement admin auth endpoints (/admin/login, /admin/list)
- [x] Add health check endpoint /health
- [x] Add CORS, config via env
- [x] Add tests for endpoints
- [x] Dockerfile for backend

### 2. Frontend basic
- [x] Create Next.js app with Tailwind
- [x] Implement home page (signup form)
- [x] Implement admin login and admin list page
- [x] Connect to backend (NEXT_PUBLIC_API_URL)
- [x] Add validation & loading states

### 3. Local dev experience
- [x] docker-compose.dev (optional) for local quickstart
- [x] Scripts in README to run local backend & frontend

### 4. Deployment
- [x] Deploy Supabase project and create table (instructions in README)
- [x] Deploy backend to Render (Docker), set env
- [x] Deploy frontend to Vercel, set env
- [ ] Verify live frontend <-> backend integration

### 5. Tests & basic CI
- [x] Add tests verifying:
    - [x] POST /waitlist accepts new email and rejects duplicate
    - [x] POST /admin/login returns token for correct password
- [x] Add github/workflows/ci.yml

### 6. Documentation & finalization
- [x] README with live URLs, admin password, and local dev steps
- [x] Clean up and final commit

## Proposed Plan — Waitlist App Enhancements (Revised)

### Overview
Enhance the Waitlist App by collecting optional first name and last name from users, and automatically detecting their country from the request. Implement filtering and search on the admin page. Redesign the frontend, backend, and email with a creative aesthetic, dark mode, and animations. Finally, automate database table creation during Docker build/startup.

### Checklist

#### 1. User Information & Database Update
- [x] Update `backend/app/models.py`: Add `first_name` (String, nullable), `last_name` (String, nullable), `country` (String, nullable) to the `Waitlist` model.
- [x] Update `backend/app/schemas.py`: Include `first_name` and `last_name` in `WaitlistCreate` and all three new fields (`first_name`, `last_name`, `country`) in `WaitlistOut` Pydantic models.
- [x] Update `backend/app/crud.py`: Adjust functions to handle the new fields.
- [x] Implement Country Detection: Add a utility in the backend to detect the user's country based on the request's IP address (e.g., using a geo-IP library or a third-party API).
- [x] Update `backend/app/routes/waitlist.py`: Integrate country detection into the POST endpoint.
- [x] Update `frontend/src/app/page.tsx`: Add optional input fields for first name and last name (remove country input).
- [x] Update `frontend/src/app/admin/page.tsx`: Display the new user information (first name, last name, country) in the admin list.
- [x] Update `backend/tests/test_waitlist.py`: Adjust tests to account for the new fields and country detection.

#### 2. Automated Database Table Creation (Alembic)
- [x] Initialize Alembic for database migrations in the `backend/` directory.
- [x] Generate an initial migration script for the `Waitlist` model.
- [x] Add a command to `backend/Dockerfile` to run Alembic migrations on container startup.
- [x] Update `README.md` with instructions for managing Alembic migrations.

#### 3. Admin Page Filtering and Search
- [x] Update `backend/app/routes/admin.py`: Modify the `/admin/list` endpoint to accept optional query parameters for filtering (e.g., by email, first name, last name, country) and a general search term.
- [x] Update `backend/app/crud.py`: Implement the logic to apply these filters and search queries to the database results.
- [x] Update `frontend/src/app/admin/page.tsx`: Add input fields for filtering and searching, and update the data fetching logic to send these parameters to the backend.

#### 4. Redesign, Dark Mode & Animations
- [ ] **Frontend Redesign:**
    - [x] Implement a creative and modern design for the signup and admin pages.
    - [x] Add a dark mode toggle and apply dark mode styling across the frontend.
    - [x] Incorporate subtle animations for user interactions (e.g., form submission, loading states, page transitions).
- [ ] **Email Redesign:**
    - [x] Update `backend/app/utils/email.py`: Use a more creative and visually appealing HTML template for the welcome email.
- [ ] **Backend (Minor Aesthetic):**
    - [x] (Optional) Review API responses for consistency and clarity, but no major functional redesign.

#### 5. Verification & Finalization
- [ ] Thoroughly verify all new features locally.
- [ ] Update `PLAN.md` with the new checklist and mark completed tasks.
- [ ] Commit changes frequently with descriptive messages.
