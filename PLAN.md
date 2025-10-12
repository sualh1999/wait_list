# PLAN — Waitlist App

Status: In Progress

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
- [ ] Create Next.js app with Tailwind
- [ ] Implement home page (signup form)
- [ ] Implement admin login and admin list page
- [ ] Connect to backend (NEXT_PUBLIC_API_URL)
- [ ] Add validation & loading states

### 3. Local dev experience
- [ ] docker-compose.dev (optional) for local quickstart
- [ ] Scripts in README to run local backend & frontend

### 4. Deployment
- [ ] Deploy Supabase project and create table (instructions in README)
- [ ] Deploy backend to Render (Docker), set env
- [ ] Deploy frontend to Vercel, set env
- [ ] Verify live frontend <-> backend integration

### 5. Documentation & finalization
- [ ] README with live URLs, admin password, and local dev steps
- [ ] Clean up and final commit
