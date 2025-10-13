FROM python:3.11-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
COPY ./alembic.ini /app/
COPY ./alembic /app/alembic

EXPOSE 8000

# Run migrations and then start the app
CMD ["/bin/bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
