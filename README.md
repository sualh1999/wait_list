# Waitlist App

This is a waitlist application with a FastAPI backend and a Next.js frontend.

## Local Development

### Backend Setup

It is recommended to use a Python virtual environment for the backend. To create and activate one:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

## Database Setup (Supabase)

This project uses PostgreSQL, and it's recommended to use Supabase for easy setup.

1.  **Create a Supabase Project:**
    *   Go to [Supabase](https://supabase.com/) and create a new project.
    *   Note down your project's region and database password.

2.  **Get your DATABASE_URL:**
    *   In your Supabase project dashboard, navigate to `Project Settings` -> `Database`.
    *   Under the `Connection String` section, copy the `URI` (connection string).
    *   It will look something like: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`
    *   Replace `[YOUR-PASSWORD]` with your actual database password.

3.  **Create the `waitlist` table:**
    *   In your Supabase project dashboard, navigate to `SQL Editor`.
    *   Run the following SQL queries to create the `waitlist` table:

    ```sql
    create extension if not exists "uuid-ossp";

    create table if not exists waitlist (
      id uuid primary key default gen_random_uuid(),
      email text unique not null,
      created_at timestamp with time zone default now()
    );
    ```

4.  **Configure CORS (if using Supabase functions/Edge Functions):**
    *   If you plan to use Supabase Edge Functions or other Supabase-hosted services that require CORS, you might need to configure it in your Supabase project settings under `API` -> `CORS`.
    *   Add your frontend URL (e.g., `http://localhost:3000`, `https://your-frontend-domain.vercel.app`) to the allowed origins.
