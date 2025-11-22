FROM python:3.11-slim

LABEL maintainer="Security Research Team"
LABEL description="dicti0nary-attack - Non-Dictionary Password Research Tool"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Create output directory
RUN mkdir -p /app/output /app/wordlists

# Expose web interface port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DICTI0NARY_OUTPUT_DIR=/app/output

# Default command (can be overridden)
CMD ["dicti0nary", "--help"]
