# Simple Dockerfile for Python Flask application
# 
# Key concepts:
# - FROM: Specifies the base image to use
# - WORKDIR: Sets the working directory inside the container
# - COPY: Copies files from host to container
# - RUN: Executes commands during the build process
# - EXPOSE: Documents which ports are intended to be published
# - CMD: Defines the default command to run when the container starts

# Use Python 3.9 slim image as base to keep the image size small
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
# (We copy this first to leverage Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Document that the container will listen on port 5000
EXPOSE 5000

# Command to run when container starts
CMD ["python", "app.py"]
