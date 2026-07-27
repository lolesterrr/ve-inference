FROM python:3.10-slim

# Install only what is absolutely necessary
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ git libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Use a smaller pip install
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PORT=8080
# Force garbage collection and smaller memory footprint
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
