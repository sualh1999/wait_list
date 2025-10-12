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
