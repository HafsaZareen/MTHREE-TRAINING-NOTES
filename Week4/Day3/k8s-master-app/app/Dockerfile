# Use Python 3.9 instead of slim to avoid needing to install packages
# The non-slim version already has many utilities installed
FROM python:3.9

# Add metadata to the image
LABEL maintainer="k8s-zero-hero@example.com"
LABEL version="1.0.0"
LABEL description="Kubernetes Zero to Hero Master Application"

# Set working directory inside the container
WORKDIR /app

# Create volume mount points with proper permissions
RUN mkdir -p /data /config /logs && \
    chmod 777 /data /config /logs

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
RUN chmod +x app.py

# Expose the port the app will run on
EXPOSE 5000

# Add custom health check script
RUN echo '#!/bin/sh' > /healthcheck.sh && \
    echo 'curl -s http://localhost:5000/api/health || exit 1' >> /healthcheck.sh && \
    chmod +x /healthcheck.sh

# Set up a non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app /data /config /logs

# Switch to the non-root user
USER appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_NAME="K8s Master App" \
    APP_VERSION="1.0.0" \
    ENVIRONMENT="production" \
    DATA_PATH="/data" \
    CONFIG_PATH="/config" \
    LOG_PATH="/logs"

# Start the application
CMD ["python", "app.py"]

# Add HEALTHCHECK instruction to check container health
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD /healthcheck.sh
