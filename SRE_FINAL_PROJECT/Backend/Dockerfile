# Stage 1: Build and cache dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --user --no-cache-dir sentence-transformers==2.2.2

# Pre-download SentenceTransformer model
RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('/app/model')"

# Stage 2: Runtime image
FROM python:3.9-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy pre-cached model
COPY --from=builder /app/model /app/model

# Copy application files
COPY Flask_backend/app.py .
COPY Dataset/ipc_sections_updated.csv ./Dataset/
COPY Flask_backend/embeddings.pt ./embeddings.pt  

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DB_PATH=/app/Database/law_enforcement.db \
    DATASET_PATH=/app/Dataset/ipc_sections_updated.csv \
    UPLOAD_FOLDER=/app/Uploads/Evidence \
    SENTENCE_TRANSFORMERS_HOME=/app/model \
    PATH=/root/.local/bin:$PATH

# Create directories
RUN mkdir -p /app/Uploads/Evidence /app/Database

EXPOSE 5000

# Run with Gunicorn (minimal workers, timeout, and logging)
CMD ["gunicorn", "--workers", "1", "--timeout", "300", "--bind", "0.0.0.0:5000", "--log-level", "info", "app:app"]