FROM python:3.13-slim-bookworm

ENV PYTHONPATH=/qsmith/app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic ./alembic/

COPY app/ ./app/

ENTRYPOINT ["uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "9082", "--reload"]

