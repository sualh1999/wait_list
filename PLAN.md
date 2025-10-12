# PLAN — Waitlist App

Status: In Progress

## Overview
Build Waitlist App: FastAPI backend + Next.js frontend + Supabase + Resend + Docker (backend). Deploy backend to Render and frontend to Vercel.

## Checklist

### 0. Repo initialize
- [x] Create repo skeleton, .gitignore, .env.example, README.md, PLAN.md

### 1. Backend basic
- [ ] Create FastAPI app skeleton (app/main.py)
- [ ] Setup async SQLAlchemy + models + migrations notes
- [ ] Implement /waitlist POST endpoint
- [ ] Implement duplicate email check (db unique constraint)
- [ ] Implement Resend email util (email on success)
- [ ] Implement admin auth endpoints (/admin/login, /admin/list)
- [ ] Add health check endpoint /health
- [ ] Add CORS, config via env
- [ ] Add tests for endpoints
- [ ] Dockerfile for backend

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
