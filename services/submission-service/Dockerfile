FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads && chown -R appuser:appuser uploads

USER appuser

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

