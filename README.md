# Waitlist App

This is a waitlist application with a FastAPI backend and a Next.js frontend.

## Live URLs

*   **Frontend:** [Your Vercel Frontend URL Here]
*   **Backend:** [Your Render Backend URL Here]

## Admin Access

*   **Admin Password:** `[Your ADMIN_PASSWORD from .env]` (Please keep this secure in production)

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

### 4. Database Migrations (Alembic)

This project uses Alembic for database migrations. Migrations are automatically applied when the Docker backend service starts.

To generate new migrations (after making changes to `backend/app/models.py`):

1.  **Activate the backend virtual environment:**
    ```bash
    cd backend
    source .venv/bin/activate
    ```
2.  **Generate a new migration script:**
    ```bash
    DATABASE_URL="postgresql://user:password@localhost:5432/waitlist_db" \
    alembic revision --autogenerate -m "Description of your changes"
    ```
    *Note: You need to provide a valid `DATABASE_URL` for Alembic to connect to your database and detect changes.*
3.  **Review and edit the generated migration script** in `backend/alembic/versions/` if necessary.
4.  **Apply migrations (for local development outside Docker):**
    ```bash
    DATABASE_URL="postgresql://user:password@localhost:5432/waitlist_db" \
    alembic upgrade head
    ```
    *When running with Docker Compose, migrations are applied automatically.*

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

### 4. Backend Deployment (Render)

To deploy the FastAPI backend to Render:

1.  **Create a new Web Service on Render:**
    *   Go to [Render](https://render.com/) and create a new `Web Service`.
    *   Connect your GitHub repository.
    *   Select the `backend` folder as the root directory for the service.

2.  **Configure the service:**
    *   **Build Command:** Leave empty (Render will detect the `Dockerfile`).
    *   **Start Command:** Leave empty (Render will use `CMD` from `Dockerfile`).
    *   **Runtime:** Docker
    *   **Port:** `8000`
    *   **Health Check Path:** `/health`

3.  **Add Environment Variables:**
    *   In Render, go to your service settings and add the following environment variables. These should match the values from your `.env` file, but ensure they are set directly in Render's dashboard for security.
        *   `DATABASE_URL`: Your Supabase connection string (e.g., `postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres`).
        *   `RESEND_API_KEY`: Your Resend API key.
        *   `ADMIN_PASSWORD`: Your chosen admin password.
        *   `ALLOWED_ORIGINS`: A comma-separated list of allowed origins (e.g., `https://your-frontend-domain.vercel.app,http://localhost:3000`).

4.  **Deploy:** Trigger a deploy. Once deployed, note the live URL of your backend service.

5.  **Verification:**
    *   Access the `/health` endpoint of your deployed backend (e.g., `https://your-backend.onrender.com/health`). It should return `{"status": "ok"}`.
    *   Test the `/waitlist` endpoint using a tool like Postman or `curl` to ensure it accepts new email submissions.

### 5. Frontend Deployment (Vercel)

To deploy the Next.js frontend to Vercel:

1.  **Create a new Project on Vercel:**
    *   Go to [Vercel](https://vercel.com/) and create a new project.
    *   Connect your GitHub repository.
    *   Select the `frontend` folder as the root directory for the project.

2.  **Configure Environment Variables:**
    *   In your Vercel project settings, go to `Environment Variables`.
    *   Add `NEXT_PUBLIC_API_URL` and set its value to the URL of your deployed Render backend (e.g., `https://your-backend.onrender.com`).

3.  **Deploy:** Trigger a deploy. Once deployed, note the live URL of your frontend service.

4.  **Verification:**
    *   Access your deployed frontend URL. The home page should load.
    *   Try submitting an email to the waitlist. It should successfully post to your deployed backend.

## Repository Access (for `chapimenge3`)

If this repository is private, please invite `chapimenge3` as a collaborator to grant access.
