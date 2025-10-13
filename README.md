# Waitlist App

This is a waitlist application with a FastAPI backend and a Next.js frontend.

## Live URL

The application is live at: **https://wait-list-1j29.vercel.app/**

## Admin Access

-   **Admin URL:** [https://wait-list-1j29.vercel.app/admin](https://wait-list-1j29.vercel.app/admin)
-   **Admin Password:** `123456`

**Warning:** It is strongly recommended to change the admin password and not to expose it in a public README file.

## Tech Stack

-   **Backend:** FastAPI, PostgreSQL, Alembic
-   **Frontend:** Next.js, React, Tailwind CSS
-   **Deployment:** Docker, Vercel (frontend), Render (backend, database)

## Database Schema

The `waitlist` table has the following structure:

| Column       | Type      | Constraints          |
| :----------- | :-------- | :------------------- |
| `id`         | `UUID`    | Primary Key, Default |
| `email`      | `String`  | Unique, Not Null     |
| `first_name` | `String`  | Nullable             |
| `last_name`  | `String`  | Nullable             |
| `country`    | `String`  | Nullable             |
| `created_at` | `DateTime`| Server Default (now())|

## Local Development

### Prerequisites

-   Docker and Docker Compose
-   Node.js and npm

### 1. Backend

1.  Create a `.env` file in the project root. You can copy `.env.example`.
2.  Run `docker-compose -f docker-compose.dev.yml up --build -d`.
3.  The backend will be available at `http://localhost:8000`.

### 2. Frontend

1.  `cd frontend`
2.  `npm install`
3.  Create a `.env.local` file with `NEXT_PUBLIC_API_URL=http://localhost:8000`.
4.  `npm run dev`
5.  The frontend will be available at `http://localhost:3000`.

---