# Waitlist App

This is a waitlist application with a FastAPI backend and a Next.js frontend.

## Local Development

This project can be run locally using Docker Compose for the backend and a separate process for the Next.js frontend.

### Prerequisites

*   Docker and Docker Compose
*   Node.js and npm (for frontend)
*   Python 3.11+ (for backend development outside Docker)

### 1. Backend Setup (Docker Compose)

1.  **Create a `.env` file** in the project root (`waitlist-app/`) based on `.env.example` and fill in your `RESEND_API_KEY` and `ADMIN_PASSWORD`.

    ```
    DATABASE_URL="postgresql://user:password@localhost:5432/waitlist_db" # This will be overridden by docker-compose for the backend service
    RESEND_API_KEY="re_YOUR_RESEND_API_KEY"
    ADMIN_PASSWORD="your_admin_password"
    ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8000"
    NEXT_PUBLIC_API_URL="http://localhost:8000"
    ```

2.  **Start the backend services** (PostgreSQL database and FastAPI app) using Docker Compose:

    ```bash
    docker compose -f docker-compose.dev.yml up --build -d
    ```

    This will:
    *   Build the backend Docker image.
    *   Start a PostgreSQL container (`db`).
    *   Start the FastAPI backend container (`backend`), connected to the `db` container.

3.  **Verify Backend:**
    *   The backend should be accessible at `http://localhost:8000`.
    *   You can check the health endpoint: `curl http://localhost:8000/health` (should return `{"status": "ok"}`).

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Create a `.env.local` file** in the `frontend/` directory with the following content:

    ```
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

4.  **Run the development server:**

    ```bash
    npm run dev
    ```

    The frontend should be accessible at `http://localhost:3000`.

### 3. Running Backend Tests (outside Docker)

It is recommended to use a Python virtual environment for the backend development and testing.

1.  **Create and activate a virtual environment** in the `backend/` directory:

    ```bash
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    cd ..
    ```

2.  **Install backend dependencies** (including test tools):

    ```bash
    pip install -r backend/requirements.txt pytest aiosqlite
    ```

3.  **Run tests:**

    ```bash
    source backend/.venv/bin/activate && \
    DATABASE_URL="sqlite+aiosqlite:///./test.db" \
    RESEND_API_KEY="test_resend_key" \
    ADMIN_PASSWORD="test_admin_password" \
    ALLOWED_ORIGINS="http://localhost,http://localhost:3000" \
    python3 -m pytest backend/tests
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
