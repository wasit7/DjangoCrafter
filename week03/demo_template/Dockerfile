FROM python:3.9-slim
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Create app directory
WORKDIR /app
RUN chmod -R 777 /app

# Copy the requirements file if you have it
COPY requirements.txt /app/requirements.txt
# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
# Copy the rest of the application code
COPY . /app
RUN chmod 777 /app/entrypoint.sh
# Expose port 8000 for Django
EXPOSE 8000
# Default command
CMD ["/bin/bash","/app/entrypoint.sh"]