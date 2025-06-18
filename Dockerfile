FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONPATH=/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

#auto migrations
#CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80 --reload


#CMD ["sh", "-c", "ls && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
