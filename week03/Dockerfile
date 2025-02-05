# Dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for our code
WORKDIR /usr/src/app

# Copy requirements first, for caching purposes
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our code into the container
COPY . .

# Make sure our entrypoint script is executable
RUN chmod +x entrypoint.sh

# Expose port 8000 for Django
EXPOSE 8000

# Default command
CMD ["/bin/bash", "entrypoint.sh"]
