FROM python:3.10-slim

RUN useradd -m -u 1001 appuser

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R appuser:appuser /app

EXPOSE 8080

ENV PYTHONPATH=/app

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
